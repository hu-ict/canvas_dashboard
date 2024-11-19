document.getElementById('logout-button').addEventListener('click', function() {
    fetch('/auth/logout', {
        method: 'GET',
        credentials: 'same-origin'
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/auth/login';
        } else {
            alert("Uitloggen mislukt, probeer opnieuw.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Er is een probleem opgetreden bij het uitloggen.");
    });
});
