// DIALOG BOX=================================================================
function showDialog(message) {
    document.getElementById("dialog-message").innerText = message;
    document.getElementById("overlay").style.display = "block";
    document.getElementById("dialog-box").style.display = "block";
}
function closeDialog() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("dialog-box").style.display = "none";
}


// FORM VALIDATION=============================================================
function validateEmail(email) {
    // Regular expression for validating email addresses
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}
const form = document.getElementById("signup-form");
form.addEventListener("submit", function(event) {
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    if (!validateEmail(email)) {
        event.preventDefault(); // Prevent form submission
        showDialog("Invalid email address");
    }
    if (!phone.startsWith("254")) {
        event.preventDefault(); // Prevent form submission
        showDialog("Phone number must start with 254 E.g. 254700000000");
    }
    if (phone.length <12 ) {
        event.preventDefault(); // Prevent form submission
        showDialog("Invalid phone number. Phone number must start with 254 E.g. 254700000000");
    }
});
