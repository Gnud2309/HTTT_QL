function validateField(fieldId, errorId, errorMessage) {
    
    const field = document.getElementById(fieldId);
    const errorSpan = document.getElementById(errorId);

    // Regular Expression for valid name (letters, spaces, and Vietnamese characters)
    const nameRegex = /^[a-zA-Z\sáàạảãâấầậẩẫăắằặẳẵéèẹẻẽêếềệểễíìịỉĩóòọỏõôốồộổỗơớờợởỡúùụủũôóòọỏõđýỳỵỷỹç]+$/i;

    if (!field.value.trim()) {
        errorSpan.textContent = errorMessage;
    } else if (!nameRegex.test(field.value.trim())) {
        errorSpan.textContent = "Name must only contain letters, spaces, and Vietnamese characters.";
    } else {
        errorSpan.textContent = '';
    }
}


function validateEmail(fieldId, errorId) {
    const field = document.getElementById(fieldId);
    const errorSpan = document.getElementById(errorId);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!field.value.trim()) {
        errorSpan.textContent = "Email is required.";
    } else if (!emailRegex.test(field.value.trim())) {
        errorSpan.textContent = "Invalid email format.";
    } else {
        errorSpan.textContent = '';
    }
}

function validatePhone(fieldId, errorId) {
    const field = document.getElementById(fieldId);
    const errorSpan = document.getElementById(errorId);
    const phoneRegex = /^[0-9]{10,12}$/;

    if (!field.value.trim()) {
        errorSpan.textContent = "Phone number is required.";
    } else if (!phoneRegex.test(field.value.trim())) {
        errorSpan.textContent = "Phone number must be 10-12 digits.";
    } else {
        errorSpan.textContent = '';
    }
}