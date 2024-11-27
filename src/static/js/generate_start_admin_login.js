document.getElementById('admin-login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const password = document.getElementById('password').value;

    if (!password) {
        alert('Wachtwoord is verplicht!');
        return;
    }

    fetch('/generate/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/generate/start';
        } else {
            throw new Error('Ongeldig wachtwoord.');
        }
    })
    .catch(error => {
        console.error('Fout bij inloggen:', error);
        alert('Inloggen mislukt: ' + error.message);
    });
});
