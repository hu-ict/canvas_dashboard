document.getElementById('generate-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = document.getElementById('generate-form');
    const submitButton = document.getElementById('submit-button');
    const loader = document.getElementById('loader');
    const successMessage = document.getElementById('success-message');

    const newInstance = document.getElementById('new_instance').value;
    const category = document.getElementById('category').value;
    const canvasCourseId = document.getElementById('canvas_course_id').value;

    if (!newInstance || !category || !canvasCourseId) {
        alert('Alle velden zijn verplicht!');
        return;
    }

    Array.from(form.elements).forEach(input => input.disabled = true);
    submitButton.disabled = true;
    loader.style.display = 'block';
    successMessage.style.display = 'none';

    let dots = 0;
    const loaderInterval = setInterval(() => {
        dots = (dots + 1) % 4;
        loader.textContent = `Bezig met verwerken${'.'.repeat(dots)}`;
    }, 500);

    fetch('/generate/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            new_instance: newInstance,
            category: category,
            canvas_course_id: canvasCourseId
        })
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(loaderInterval);
        loader.style.display = 'none';
        if (data.status === 'Success') {
            successMessage.style.display = 'block';
        } else {
            throw new Error(data.message || 'Er is iets misgegaan.');
        }
    })
    .catch(error => {
        clearInterval(loaderInterval);
        loader.style.display = 'none';
        console.error('Fout bij het genereren:', error);
        alert('Genereren mislukt: ' + error.message);
    })
    .finally(() => {
        Array.from(form.elements).forEach(input => input.disabled = false);
        submitButton.disabled = false;
    });
});

document.getElementById('logout-button').addEventListener('click', function() {
    fetch('/generate/logout', {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/generate/login'; // Redirect to login page
        } else {
            throw new Error('Uitloggen mislukt.');
        }
    })
    .catch(error => {
        console.error('Fout bij uitloggen:', error);
        alert('Uitloggen mislukt: ' + error.message);
    });
});