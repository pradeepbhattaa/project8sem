document.addEventListener('DOMContentLoaded', function() {
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

    



// Handle form submission
 document.getElementById('email-form').addEventListener('submit', function(event) {


    const isEmailValid = validateEmail('email', 'email-error');
    
    
     
     

     if (  !isEmailValid     ) {
         event.preventDefault();
     }
 });

});