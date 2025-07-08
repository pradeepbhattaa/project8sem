document.addEventListener('DOMContentLoaded', function() {
    // Hide messages after 3 seconds
    setTimeout(function() {
        const messageContainer = document.getElementById('errorMessageId');
        if (messageContainer) {
            messageContainer.style.display = 'none';
        }
    }, 3000);

    // Validate Name Field
    function validateName(inputFieldId, errorMessageId) {
        const inputField = document.getElementById(inputFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const inputValue = inputField.value.trim();
        const nameRegex = /^[a-zA-Z]+$/;

        if (inputValue === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (!nameRegex.test(inputValue)) {
            errorMessage.textContent = 'Please enter a valid name';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Validate Date of Birth
    function validateDOB(dobFieldId, errorMessageId) {
        const dobField = document.getElementById(dobFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const dobValue = dobField.value;
        if (!dobValue) {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        }
        const dobDate = new Date(dobValue);
        const today = new Date();
        const minAge = 18;
        const minDateOfBirth = new Date(today.getFullYear() - minAge, today.getMonth(), today.getDate());

        if (dobDate > minDateOfBirth) {
            errorMessage.textContent = 'You must be at least 18 years old';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Validate Phone Number
    function validatePhoneNumber(phoneNumberFieldId, errorMessageId) {
        const phoneNumberField = document.getElementById(phoneNumberFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const phoneNumber = phoneNumberField.value.trim();

        if (phoneNumber === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (phoneNumber.length !== 10 || isNaN(phoneNumber)) {
            errorMessage.textContent = 'Phone number must be exactly 10 digits';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Validate Email
    function validateEmail(emailFieldId, errorMessageId) {
        const emailField = document.getElementById(emailFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const emailValue = emailField.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (emailValue === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (!emailRegex.test(emailValue)) {
            errorMessage.textContent = 'Please enter a valid email address';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Validate Citizenship Number
    function validateCitizenshipNumber(citizenshipFieldId, errorMessageId) {
        const citizenshipField = document.getElementById(citizenshipFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const citizenshipNumber = citizenshipField.value.trim();

        if (citizenshipNumber === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (isNaN(citizenshipNumber)) {
            errorMessage.textContent = 'Citizenship number must be a number';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Validate Voter ID Number
    function validateVoterID(voterIDFieldId, errorMessageId) {
        const voterIDField = document.getElementById(voterIDFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const voterIDNumber = voterIDField.value.trim();

        if (voterIDNumber === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (isNaN(voterIDNumber)) {
            errorMessage.textContent = 'Voter ID number must be a number';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Validate Municipality
    function validateMunicipal(municipalFieldId, errorMessageId) {
        const municipalField = document.getElementById(municipalFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const municipalValue = municipalField.value.trim();

        if (municipalValue === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (/\d/.test(municipalValue)) {
            errorMessage.textContent = 'Municipality name cannot contain numbers';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Validate Ward Number
    function validateWard(wardFieldId, errorMessageId) {
        const wardField = document.getElementById(wardFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const wardNumber = wardField.value.trim();

        if (wardNumber === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (isNaN(wardNumber)) {
            errorMessage.textContent = 'Ward number must be a number';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Handle form submission
    document.getElementById('register-form').addEventListener('submit', function(event) {
        const isPhoneNumberValid = validatePhoneNumber('phone_number', 'phone-error');
        const isEmailValid = validateEmail('email', 'email-error');
        const isPasswordValid = validatePassword('password', 'password-error');
        const isConfirmPasswordValid = validateConfirmPassword('password', 'confirm_password', 'confirm-password-error');
        const isCitizenshipNumberValid = validateCitizenshipNumber('citizenship_number', 'citizen-error');
        const isVoterIDValid = validateVoterID('voter_id', 'voter-error');
        const isMunicipalValid = validateMunicipal('municipality', 'municipal-error');
        const isWardValid = validateWard('ward_no', 'ward-error');

        if (!isPhoneNumberValid || !isEmailValid || !isPasswordValid || !isConfirmPasswordValid || !isCitizenshipNumberValid || !isVoterIDValid || !isMunicipalValid || !isWardValid) {
            event.preventDefault();
        }
    });

    // Handle "Next" button click
    document.getElementById('next-btn').addEventListener('click', function() {
        const isFirstNameValid = validateName('first-name', 'first-name-error');
        const isLastNameValid = validateName('last-name', 'last-name-error');
        const isDOBValid = validateDOB('dob', 'dob-error');
        const isPhoneNumberValid = validatePhoneNumber('phone_number', 'phone-error');
        const isEmailValid = validateEmail('email', 'email-error');
        const isCitizenshipNumberValid = validateCitizenshipNumber('citizenship_number', 'citizen-error');
        const isVoterIDValid = validateVoterID('voter_id', 'voter-error');
        const isMunicipalValid = validateMunicipal('municipality', 'municipal-error');
        const isWardValid = validateWard('ward_no', 'ward-error');

        if (isFirstNameValid && isLastNameValid && isDOBValid && isPhoneNumberValid && isEmailValid && isCitizenshipNumberValid && isVoterIDValid && isMunicipalValid && isWardValid) {
            document.getElementById('section-1').classList.remove('show');
            document.getElementById('section-2').classList.add('show');
            document.querySelector('.step-circle:nth-child(2)').classList.add('active');
        }
    });

    // Handle "Back" button click
    document.querySelector('.back-btn').addEventListener('click', function() {
        document.getElementById('section-2').classList.remove('show');
        document.getElementById('section-1').classList.add('show');
    });
});
