



document.addEventListener('DOMContentLoaded', function() {
    
    // Function to handle "Next" button click
    document.getElementById('nextBtn').addEventListener('click', function() {
        // Validate fields on the current page
        const isFirstNameValid = validateName('first-name', 'first-name-error');
        const isLastNameValid = validateName('last-name', 'last-name-error');
        const isDOBValid = validateDOB('dob', 'dob-error');
        const isPhoneNumberValid = validatePhoneNumber('phone_number', 'phone-error');
        const isCitizenshipNumberValid = validateNumber('citizenship_number', 'citizen-error');
        const isVoterIDValid = validateNumber('voter_id', 'voter-error');

        // Proceed to next page if all validations pass
        if (isFirstNameValid && isLastNameValid && isDOBValid && isPhoneNumberValid && isCitizenshipNumberValid && isVoterIDValid) {
            document.getElementById('page1').style.display = 'none';
            document.getElementById('page2').style.display = 'block';
            document.getElementById('prevBtn').style.display = 'block';
            document.getElementById('submitBtn').style.display = 'block';
        }
    });

    // Function to handle form submission
    document.getElementById('registrationForm').addEventListener('submit', function(event) {
        // Validate fields on the entire form before submitting
        const isFirstNameValid = validateName('first-name', 'first-name-error');
        const isLastNameValid = validateName('last-name', 'last-name-error');
        const isDOBValid = validateDOB('dob', 'dob-error');
        const isPhoneNumberValid = validatePhoneNumber('phone_number', 'phone-error');
        const isCitizenshipNumberValid = validateNumber('citizenship_number', 'citizen-error');
        const isVoterIDValid = validateNumber('voter_id', 'voter-error');

        // If any validation fails, prevent form submission
        if (!isFirstNameValid || !isLastNameValid || !isDOBValid || !isPhoneNumberValid || !isCitizenshipNumberValid || !isVoterIDValid) {
            event.preventDefault();
        }
    });

    // Function to validate name fields (first name and last name)
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
            errorMessage.textContent = 'Please enter a valid name (only alphabets)';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Function to validate date of birth
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

    // Function to validate phone number
    function validatePhoneNumber(phoneNumberFieldId, errorMessageId) {
        const phoneNumberField = document.getElementById(phoneNumberFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const phoneNumber = phoneNumberField.value.trim();

        if (phoneNumber === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (!phoneNumber.startsWith('9') || phoneNumber.length !== 10 || isNaN(phoneNumber)) {
            errorMessage.textContent = 'Phone number must start with 9 and be exactly 10 digits';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Function to validate citizenship number and voter ID (both should contain only digits)
    function validateNumber(inputFieldId, errorMessageId) {
        const inputField = document.getElementById(inputFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const inputValue = inputField.value.trim();
        const numberRegex = /^\d+$/;

        if (inputValue === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (!numberRegex.test(inputValue)) {
            errorMessage.textContent = 'Please enter a valid number';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Function to handle "Previous" button click (if needed)
    document.getElementById('prevBtn').addEventListener('click', function() {
        document.getElementById('page2').style.display = 'none';
        document.getElementById('page1').style.display
        = 'block';
        document.getElementById('prevBtn').style.display = 'none';
        document.getElementById('submitBtn').style.display = 'none';
    });

    // Additional functions for form validation and navigation

    // Function to handle form submission
    document.getElementById('registrationForm').addEventListener('submit', function(event) {
        // Validate fields on the entire form before submitting
        const isFirstNameValid = validateName('first-name', 'first-name-error');
        const isLastNameValid = validateName('last-name', 'last-name-error');
        const isDOBValid = validateDOB('dob', 'dob-error');
        const isPhoneNumberValid = validatePhoneNumber('phone_number', 'phone-error');
        const isCitizenshipNumberValid = validateNumber('citizenship_number', 'citizen-error');
        const isVoterIDValid = validateNumber('voter_id', 'voter-error');

        // If any validation fails, prevent form submission
        if (!isFirstNameValid || !isLastNameValid || !isDOBValid || !isPhoneNumberValid || !isCitizenshipNumberValid || !isVoterIDValid) {
            event.preventDefault();
        }
    });

    // Function to validate name fields (first name and last name)
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
            errorMessage.textContent = 'Please enter a valid name (only alphabets)';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Function to validate date of birth
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

    // Function to validate phone number
    function validatePhoneNumber(phoneNumberFieldId, errorMessageId) {
        const phoneNumberField = document.getElementById(phoneNumberFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const phoneNumber = phoneNumberField.value.trim();

        if (phoneNumber === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (!phoneNumber.startsWith('9') || phoneNumber.length !== 10 || isNaN(phoneNumber)) {
            errorMessage.textContent = 'Phone number must start with 9 and be exactly 10 digits';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Function to validate citizenship number and voter ID (both should contain only digits)
    function validateNumber(inputFieldId, errorMessageId) {
        const inputField = document.getElementById(inputFieldId);
        const errorMessage = document.getElementById(errorMessageId);
        const inputValue = inputField.value.trim();
        const numberRegex = /^\d+$/;

        if (inputValue === '') {
            errorMessage.textContent = 'This field is required';
            errorMessage.style.display = 'block';
            return false;
        } else if (!numberRegex.test(inputValue)) {
            errorMessage.textContent = 'Please enter a valid number';
            errorMessage.style.display = 'block';
            return false;
        } else {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
            return true;
        }
    }

    // Function to handle "Previous" button click (if needed)
    document.getElementById('prevBtn').addEventListener('click', function() {
        document.getElementById('page2').style.display = 'none';
        document.getElementById('page1').style.display = 'block';
        document.getElementById('prevBtn').style.display = 'none';
        document.getElementById('submitBtn').style.display = 'none';
    });
});
