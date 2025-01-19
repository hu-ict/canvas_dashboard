document.getElementById('inloggen').addEventListener('click', function () {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                alert('Login successful!');

                // Voeg de Authorization header toe voor dashboard request
                return fetch('/dashboard', {
                    method: 'GET',
                    headers: {'Authorization': `Bearer ${data.access_token}`}
                });
            } else {
                throw new Error(data.message || "Login failed");
            }
        })
        .then(dashboardResponse => {
            if (!dashboardResponse.ok) throw new Error("Failed to fetch dashboard role");
            return dashboardResponse.json();
        })
        .then(dashboardData => {
            if (dashboardData.role === 'student') {
                window.location.href = '/select_course';
            } else if (dashboardData.role === 'teacher') {
                window.location.href = '/select_course';
            } else {
                alert('Unknown role.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message || 'An error occurred during login. Please try again.');
        });
});