// static/myapp/js/face_detection.js

/* ---------- helper: toast‑style message -------------------------------- */
function showMessage(type, txt) {
  let wrap = document.getElementById('message-container');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.id = 'message-container';
    document.body.prepend(wrap);
  }

  const alert = document.createElement('div');
  alert.className = `alert ${type}`;
  alert.innerHTML = `
    <span class="closebtn" onclick="this.parentElement.remove()">×</span>
    ${txt}
  `;
  wrap.appendChild(alert);
  setTimeout(() => alert.remove(), 4000);
}

/* ---------- 1. Load face-api models ----------------------------------- */
async function loadFaceApiModels() {
  if (!window.faceapi) {
    showMessage('error', 'face‑api.js missing');
    return false;
  }
  const URL = '/static/myapp/models';
  try {
    await Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri(URL),
      faceapi.nets.faceLandmark68Net.loadFromUri(URL),
      faceapi.nets.faceRecognitionNet.loadFromUri(URL),
      faceapi.nets.faceExpressionNet.loadFromUri(URL)
    ]);
    console.log('models ready');
    return true;
  } catch (e) {
    console.error(e);
    showMessage('error', 'model load failed');
    return false;
  }
}

/* ---------- 2. Detect descriptor from KYC image ------------------------ */
async function detectFaceDescriptor(fileInput, hiddenId, previewId) {
  const file = fileInput.files[0];
  if (!file) return;
  const img = new Image();
  img.src = URL.createObjectURL(file);

  img.onload = async () => {
    const det = await faceapi.detectSingleFace(img, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceDescriptor();

    const hid = document.getElementById(hiddenId);
    const pre = document.getElementById(previewId);

    if (det) {
      hid.value = JSON.stringify(Array.from(det.descriptor));
      if (pre) {
        pre.src = img.src;
        pre.style.display = 'block';
      }
      showMessage('success', 'Face stored.');
    } else {
      showMessage('warning', 'No face detected.');
      hid.value = '';
      if (pre) pre.style.display = 'none';
      fileInput.value = '';
    }

    URL.revokeObjectURL(img.src);
  };
}

/* ---------- 3. Liveness Check: Sequential Challenges ------------------ */
const FRAME_MS = 120;
const TIMEOUT_MS = 10000;
const PITCH_THRESH = 10;
const YAW_THRESH = 10;
const MOUTH_OPEN_THRESH = 0.3;

function avgX(pts) {
  return pts.reduce((sum, p) => sum + p.x, 0) / pts.length;
}

function delay(ms) {
  return new Promise(res => setTimeout(res, ms));
}

async function runLivenessChallenge(videoEl, canvasEl, conditionFn, promptText, successText) {
  showMessage('info', promptText);
  const opt = new faceapi.TinyFaceDetectorOptions({ inputSize: 320, scoreThreshold: 0.3 });
  const ctx = canvasEl.getContext('2d', { willReadFrequently: true });

  const start = Date.now();
  let baseline = null;

  while (Date.now() - start < TIMEOUT_MS) {
    canvasEl.width = videoEl.videoWidth;
    canvasEl.height = videoEl.videoHeight;
    ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
    ctx.drawImage(videoEl, 0, 0);

    const det = await faceapi
      .detectSingleFace(canvasEl, opt)
      .withFaceLandmarks()
      .withFaceExpressions()
      .withFaceDescriptor();

    if (!det) {
      await delay(FRAME_MS);
      continue;
    }

    const lm = det.landmarks;
    const noseTip = lm.getNose()[3];
    const jaw = lm.getJawOutline();
    const jawCenter = jaw[Math.floor(jaw.length / 2)];

    const pitch = jawCenter.y - noseTip.y;

    const leftEyeX = avgX(lm.getLeftEye());
    const rightEyeX = avgX(lm.getRightEye());
    const yaw = rightEyeX - leftEyeX;

    const mouthOpen = det.expressions.mouthOpen || 0;

    if (!baseline) baseline = { pitch, yaw };

    if (conditionFn({ pitch, yaw, baseline, mouthOpen })) {
      showMessage('success', successText);
      return det.descriptor;
    }

    await delay(FRAME_MS);
  }

  showMessage('warning', `Timeout: ${promptText}`);
  return null;
}

async function captureLiveDescriptor(videoEl, canvasEl, hiddenId) {
  if (!window.faceapi) {
    showMessage('error', 'face-api not available.');
    return false;
  }

  if (!videoEl.videoWidth || !videoEl.videoHeight) {
    showMessage('error', 'Webcam not ready.');
    return false;
  }

  const hidden = document.getElementById(hiddenId);
  const challenges = [
    {
      prompt: 'Move your head UP',
      success: 'Head moved UP',
      condition: ({ pitch, baseline }) => baseline.pitch - pitch > PITCH_THRESH
    },
    {
      prompt: 'Move your head DOWN',
      success: 'Head moved DOWN',
      condition: ({ pitch, baseline }) => pitch - baseline.pitch > PITCH_THRESH
    },
    {
      prompt: 'Move your head LEFT',
      success: 'Head moved LEFT',
      condition: ({ yaw, baseline }) => yaw - baseline.yaw > YAW_THRESH
    },
    {
      prompt: 'Move your head RIGHT',
      success: 'Head moved RIGHT',
      condition: ({ yaw, baseline }) => baseline.yaw - yaw > YAW_THRESH
    },
    {
      prompt: 'Open your mouth clearly',
      success: 'Mouth open detected',
      condition: ({ mouthOpen }) => mouthOpen > MOUTH_OPEN_THRESH
    }
  ];

  // Shuffle and take any 3 challenges (one mouth open + two others)
  const shuffled = challenges.sort(() => 0.5 - Math.random());
  const selected = shuffled.filter(c => c.prompt.includes('mouth')).concat(
    shuffled.filter(c => !c.prompt.includes('mouth')).slice(0, 2)
  );

  let finalDescriptor = null;

  for (const challenge of selected) {
    const descriptor = await runLivenessChallenge(videoEl, canvasEl, challenge.condition, challenge.prompt, challenge.success);
    if (!descriptor) {
      hidden.value = '';
      return false;
    }
    finalDescriptor = descriptor; // Keep updating; final will be returned
  }

  hidden.value = JSON.stringify(Array.from(finalDescriptor));
  showMessage('success', 'Liveness verification passed.');
  return true;
}
