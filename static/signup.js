document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way

    const username = document.querySelector('#username').value;
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;
    const confirmPassword = document.querySelector('#confirm-password').value;

    // Validate password match
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Create a user object to send to the backend
    const user = {
        username: username,
        email: email,
        password: password
    };

    // Send the data to the Flask backend using fetch
    fetch('/signup', {  // Change this URL to match the Flask route
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // If signup is successful, redirect to the login page
            window.location.href = '/';
        } else {
            // If signup failed, show the error message
            alert(data.message || "Signup failed. Please try again.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
});
