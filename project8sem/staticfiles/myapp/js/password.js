document.addEventListener('DOMContentLoaded', function() {
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
            errorMessage.textContent = ' At least 8 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character';
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
    document.getElementById('password-form').addEventListener('submit', function(event) {


        const isConfirmPasswordValid = validateConfirmPassword('password', 'confirm_password', 'confirm-password-error');
       
       
        
        const isPasswordValid = validatePassword('password', 'password-error');
       

        if (    !isPasswordValid  || !isConfirmPasswordValid) {
            event.preventDefault();
        }
    });

});