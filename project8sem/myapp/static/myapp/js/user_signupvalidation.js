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

    // Validate Password
    function validatePassword(passwordFieldId, errorMessageId) {
        const passwordField = document.getElementById(passwordFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const password = passwordField.value.trim();
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

        if (password === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (!passwordRegex.test(password)) {
            errorMessage.textContent = 'Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Validate Confirm Password
    function validateConfirmPassword(passwordFieldId, confirmPasswordFieldId, errorMessageId) {
        const passwordField = document.getElementById(passwordFieldId);
        const confirmPasswordField = document.getElementById(confirmPasswordFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const password = passwordField.value.trim();
        const confirmPassword = confirmPasswordField.value.trim();

        if (confirmPassword === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (confirmPassword !== password) {
            errorMessage.textContent = 'Passwords do not match';
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

        if (  !isPhoneNumberValid || !isEmailValid || !isPasswordValid || !isConfirmPasswordValid) {
            event.preventDefault();
        }
    });

    // Handle "Next" button click
    document.getElementById('next-btn').addEventListener('click', function() {
        const isFirstNameValid = validateName('first-name', 'first-name-error');
        const isLastNameValid = validateName('last-name', 'last-name-error');
        const isDOBValid = validateDOB('dob', 'dob-error');

        if (isFirstNameValid && isLastNameValid && isDOBValid) {
            document.getElementById('section-1').classList.remove('show');
            document.getElementById('section-2').classList.add('show');
            document.querySelector('.step-circle:nth-child(2)').classList.add('active');
        }
    });

    // Handle "Back" button click
    document.querySelector('.back-btn').addEventListener('click', function() {
        document.getElementById('section-2').classList.remove('show');
        document.querySelector('.step-circle:nth-child(2)').classList.remove('active');
        document.getElementById('section-1').classList.add('show');
        document.querySelector('.step-circle:nth-child(1)').classList.add('active');
    });
});
