document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    const coursesContainer = document.getElementById('courses-list');
    const logsContainer = document.getElementById('logs-list');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(tc => tc.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');

            if (tab.dataset.tab === 'manage-courses-tab') {
                fetchCourses();
                fetchLogs();
            }
        });
    });

    function fetchCourses() {
        fetch('/get_active_courses')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    displayCourses(data.courses);
                } else {
                    console.error(data.message);
                    coursesContainer.innerHTML = `<p>Error loading courses: ${data.message}</p>`;
                }
            })
            .catch(err => {
                console.error('Error fetching courses:', err);
                coursesContainer.innerHTML = `<p>Error loading courses. Please try again later.</p>`;
            });
    }

    function displayCourses(courses) {
    const coursesContainer = document.getElementById('courses-list');
    coursesContainer.innerHTML = ''; // Clear de container

    if (courses.length === 0) {
        coursesContainer.innerHTML = '<p>No active courses found.</p>';
        return;
    }

    courses.forEach(course => {
        const courseItem = document.createElement('div');
        courseItem.classList.add('course-item');
        courseItem.innerHTML = `
            <strong>${course.name}</strong> (ID: ${course.id})<br>
            Directory: ${course.directory_name}
        `;
        coursesContainer.appendChild(courseItem);
    });
}


    function fetchLogs() {
        fetch('/get_logs')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    displayLogs(data.logs);
                } else {
                    console.error(data.message);
                    logsContainer.innerHTML = `<p>Error loading logs: ${data.message}</p>`;
                }
            })
            .catch(err => {
                console.error('Error fetching logs:', err);
                logsContainer.innerHTML = `<p>Error loading logs. Please try again later.</p>`;
            });
    }

    function displayLogs(logs) {
    const logsContainer = document.getElementById('logs-list');
    logsContainer.innerHTML = ''; // Clear de container

    if (logs.length === 0) {
        logsContainer.innerHTML = '<p>No logs found.</p>';
        return;
    }

    logs.forEach(log => {
        const logItem = document.createElement('div');
        logItem.classList.add('log-item');
        logItem.innerHTML = `
            <strong>Instance:</strong> ${log.course_instance}<br>
            <strong>Event:</strong> ${log.event}<br>
            <strong>Status:</strong> ${log.status}<br>
            <strong>Timestamp:</strong> ${new Date(log.timestamp).toLocaleString()}
        `;
        logsContainer.appendChild(logItem);
    });
}
    document.getElementById('generate-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const form = event.target;
        const newInstance = form.new_instance.value;
        const category = form.category.value;
        const canvasCourseId = form.canvas_course_id.value;

        // Existing generate start functionality
        fetch('/generate/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_instance: newInstance, category: category, canvas_course_id: canvasCourseId })
        })
            .then(response => response.json())
            .then(data => alert(data.status === 'Success' ? 'Cursus succesvol gegenereerd!' : 'Fout: ' + data.message))
            .catch(err => console.error(err));
    });

    document.getElementById('manage-courses-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const form = event.target;
        const courseInstance = form.course_instance.value;
        const eventType = form.event.value;

        fetch('/course_event', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ course_instance: courseInstance, event: eventType })
        })
            .then(response => response.json())
            .then(data => alert(data.status ? data.status : 'Fout: ' + data.error))
            .catch(err => console.error(err));
    });

    document.getElementById('logout-button').addEventListener('click', function () {
        fetch('/generate/logout', { method: 'GET' })
            .then(response => {
                if (response.ok) window.location.href = '/generate/login';
                else throw new Error('Uitloggen mislukt.');
            })
            .catch(err => alert(err.message));
    });

    // Initial fetch for active courses and logs when the page loads
    fetchCourses();
    fetchLogs();
});

function toggleDropdown(dropdownId) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.classList.toggle('show'); // Toggle de 'show' class om de inhoud in/uit te klappen
}