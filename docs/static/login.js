document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const username = document.getElementById('username').value.trim(); // Remove leading/trailing whitespace
  const password = document.getElementById('password').value.trim(); // Remove leading/trailing whitespace

  // Send login data to the backend
  fetch('/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          username: username,
          password: password
      })
  })
  .then(response => response.json())
  .then(data => {
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token); // Save the token
      window.location.href = 'home.html'; // Redirect to the home page

  }
   else {
          // If login failed, show the error message
          alert(data.msg || "Login failed. Please check your credentials.");
      }
  })
  .catch(error => {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
  });
});
