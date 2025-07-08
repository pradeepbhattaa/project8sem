/* =========================================================
   static/myapp/js/face_detection.js
   ========================================================= */

/* ---------- toast / alert helper ------------------------- */
function showMessage (type, txt) {
  let wrap = document.getElementById('message-container');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.id = 'message-container';
    document.body.prepend(wrap);
  }
  const alert = document.createElement('div');
  alert.className = `alert ${type}`;
  alert.innerHTML =
    `<span class="closebtn" onclick="this.parentElement.remove()">×</span>${txt}`;
  wrap.appendChild(alert);
  setTimeout(() => alert.remove(), 4000);
}

/* ---------- 1 load core models --------------------------- */
async function loadFaceApiModels () {
  if (!window.faceapi) { showMessage('error', 'face‑api.js missing'); return false; }
  const URL = '/static/myapp/models';
  try {
    await Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri(URL),
      faceapi.nets.faceLandmark68Net.loadFromUri(URL),
      faceapi.nets.faceRecognitionNet.loadFromUri(URL)
    ]);
    console.log('Face‑API models ready'); return true;
  } catch (e) { console.error(e); showMessage('error', 'Model load failed'); return false; }
}

/* ---------- 2 descriptor from uploaded photo ------------- */
async function detectFaceDescriptor (fileInput, hiddenId, previewId) {
  const file = fileInput.files[0]; if (!file) return;
  const img  = new Image(); img.src = URL.createObjectURL(file);

  img.onload = async () => {
    const det = await faceapi
      .detectSingleFace(img, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks().withFaceDescriptor();

    const hid = document.getElementById(hiddenId);
    const pre = document.getElementById(previewId);

    if (det) {
      hid.value = JSON.stringify(Array.from(det.descriptor));
      if (pre) { pre.src = img.src; pre.style.display = 'block'; }
      showMessage('success', 'Face stored from photo.');
    } else {
      showMessage('warning', 'No face detected – choose a clearer photo.');
      hid.value = ''; if (pre) pre.style.display = 'none'; fileInput.value = '';
    }
    URL.revokeObjectURL(img.src);
  };
}

/* ---------- 3 liveness sequence -------------------------- */
const FRAME_MS     = 120;
const TIMEOUT_MS   = 10000;
const PITCH_THRESH = 10;
const YAW_THRESH   = 8;
const MAR_THRESH   = 0.35;

const delay = ms => new Promise(r => setTimeout(r, ms));
const avgX  = pts => pts.reduce((s,p)=>s+p.x,0)/pts.length;
function mouthAspectRatio (lm) {
  const p = lm.positions;
  const v = Math.hypot(p[62].x - p[66].x, p[62].y - p[66].y);
  const h = Math.hypot(p[60].x - p[64].x, p[60].y - p[64].y);
  return v / (h + 1e-6);
}

async function runChallenge (video, canvas, condFn, prompt, success) {
  showMessage('info', prompt);

  const opt = new faceapi.TinyFaceDetectorOptions({ inputSize: 320, scoreThreshold: 0.4 });
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const t0  = Date.now();
  let base  = null;

  while (Date.now() - t0 < TIMEOUT_MS) {
    canvas.width  = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);

    const det = await faceapi
      .detectSingleFace(canvas, opt)
      .withFaceLandmarks()
      .withFaceDescriptor();

    if (!det) { await delay(FRAME_MS); continue; }

    const lm = det.landmarks;
    const pitch = lm.getJawOutline()[8].y - lm.getNose()[3].y;
    const yaw   = avgX(lm.getRightEye()) - avgX(lm.getLeftEye());
    const mar   = mouthAspectRatio(lm);

    if (!base) base = { pitch, yaw };

    if (condFn({ pitch, yaw, mar, base })) {
      showMessage('success', success);
      return det.descriptor;
    }
    await delay(FRAME_MS);
  }
  showMessage('warning', `Timeout – ${prompt}`);
  return null;
}
 async function captureLiveDescriptor(video, canvas, hiddenId) {
     if (!window.faceapi) { showMessage('error','face‑api not ready'); return false; }
     if (!video.videoWidth) { showMessage('error','Webcam not ready'); return false; }

     /* --- challenge pool (LEFT logic fixed) --- */
     const CH = [
       { prompt:'Move head DOWN',    success:'Head DOWN ✅',
         cond:({pitch,base})=> base.pitch - pitch > PITCH_THRESH },
       { prompt:'Move head UP',  success:'Head UP ✅',
         cond:({pitch,base})=> pitch - base.pitch > PITCH_THRESH },
       { prompt:'Turn head RIGHT',  success:'Head Right ✅',
         cond:({yaw,base})  => base.yaw - yaw > YAW_THRESH },   // Fixed: yaw decreases
       { prompt:'Turn head LEFT', success:'Head LEFT ✅',
         cond:({yaw,base})  => base.yaw - yaw > YAW_THRESH },   // Unchanged
       { prompt:'Open your mouth clearly', success:'Mouth open ✅',
         cond:({mar})      => mar > MAR_THRESH }
     ];

     /* pick one vertical, one horizontal, plus mouth */
     const vertical   = CH.filter(c => /UP|DOWN/.test(c.prompt));
     const horizontal = CH.filter(c => /LEFT|RIGHT/.test(c.prompt));
     const mouth      = CH.find(c => c.prompt.startsWith('Open'));

     const sel = [
       vertical[Math.floor(Math.random()*vertical.length)],
       horizontal[Math.floor(Math.random()*horizontal.length)],
       mouth
     ].sort(() => 0.5 - Math.random());          // shuffle order

     let desc = null;
     for (const c of sel) {
       desc = await runChallenge(video, canvas, c.cond, c.prompt, c.success);
       if (!desc) { document.getElementById(hiddenId).value=''; return false; }
       await delay(600);
     }

     document.getElementById(hiddenId).value = JSON.stringify(Array.from(desc));
     showMessage('success','Liveness passed 🎉');
     return true;
   }
