import threading
import glob
import os

import jwt
from flask import Blueprint, jsonify, redirect, session, send_from_directory, request, render_template_string, \
    render_template, url_for

from generate_start import main_generate
from runner import main as runner
from src.auth import login_required, role_required
from src.db.dashboards import find_dashboard_by_student_name
from src.db.db_context import db_context
from src.db.generate_data import initialize_db, read_and_import_courses
from generate_config import generate_config as main_generate_config
from flask import jsonify, request
from generate_portfolio import generate_portfolio as main_generate_portfolio
from werkzeug.exceptions import BadRequest
from src.services.remote_doc_service import upload_files_with_overwrite, find_teacher_index

import os

main_bp = Blueprint('main', __name__)


def run_in_background(instance_name, event_name):
    def task():
        try:
            print(f"Starting runner for instance {instance_name} with event {event_name}")
            runner(instance_name, event_name)
            print("Runner completed successfully")
        except Exception as e:
            print(f"Error in runner: {e}")

        try:
            with db_context() as (cursor, connection):
                initialize_db(cursor, connection)
                read_and_import_courses(cursor, connection)
                main_generate_portfolio(instance_name)
                if os.getenv('STORAGE_TYPE') == 'azure':
                    upload_files_with_overwrite()

        except Exception as e:
            print(f"Fout in database-initialisatie of import: {e}")
            return jsonify({'status': 'Error', 'message': f"Database operation failed: {e}"}), 500

    thread = threading.Thread(target=task, daemon=True)
    thread.start()


@main_bp.route("/generate/login", methods=['GET', 'POST'])
def generate_login():
    if request.method == 'POST':
        data = request.get_json()
        admin_password = data.get('password')
        if admin_password == "admin123":
            session['admin_authenticated'] = True
            return redirect(url_for('main.generate_start'))
        else:
            return jsonify({'error': 'Ongeldig wachtwoord'}), 401
    return render_template('generate_start/login.html')


@main_bp.route("/generate/start", methods=['GET', 'POST'])
def generate_start():
    if not session.get('admin_authenticated'):
        return redirect(url_for('main.generate_login'))

    if request.method == 'POST':
        data = request.get_json()  # Haal JSON-data op
        if not data:
            return jsonify({'status': 'Error', 'message': 'Geen data ontvangen'}), 400

        try:
            main_generate(data['new_instance'], data['category'], data['canvas_course_id'],
                          os.getenv('CANVAS_API_KEY'), )
            main_generate_config(data['new_instance'])
        except Exception as e:
            return jsonify({'status': 'Error', 'message': f"main_generate failed: {e}"}), 500
        try:
            run_in_background(data['new_instance'], "course_create_event")
        except Exception as e:
            print(f"Fout in runner: {e}")

        return jsonify({'status': 'Success', 'message': 'Process completed'}), 200

    return render_template('generate_start/form.html')


NIFI_AUTH_TOKEN = os.getenv("NIFI_AUTH_TOKEN", "your_default_secret_token")


@main_bp.route("/generate/start/nifi", methods=['GET', 'POST'])
def generate_start_nifi():
    auth_token = request.headers.get('Authorization')  # Token in header
    if not auth_token or auth_token != f"Bearer {NIFI_AUTH_TOKEN}":
        return jsonify({'status': 'Error', 'message': 'Unauthorized access'}), 401

    if request.method == 'POST':
        data = request.get_json()  # Haal JSON-data op
        if not data:
            return jsonify({'status': 'Error', 'message': 'Geen data ontvangen'}), 400

        try:
            main_generate(data['new_instance'], data['category'], data['canvas_course_id'], os.getenv('CANVAS_API_KEY'))
            main_generate_config(data['new_instance'])
        except Exception as e:
            return jsonify({'status': 'Error', 'message': f"main_generate failed: {e}"}), 500

        try:
            run_in_background(data['new_instance'], "course_create_event")
        except Exception as e:
            print(f"Fout in runner: {e}")

        return jsonify({
            'status': 'Success',
            'message': f'Cursus instantie {data["new_instance"]} met id {data["canvas_course_id"]} succesvol aangemaakt'
        }), 200


@main_bp.route("/course_event", methods=['POST'])
def course_event():
    if not session.get('admin_authenticated'):
        return redirect(url_for('main.generate_login'))

    try:

        data = request.get_json()

        if not data:
            raise BadRequest("Invalid JSON data provided.")

        courses_dir = os.path.abspath(os.path.join(os.getcwd(), "courses"))

        course_instance = data.get('course_instance')

        if not os.path.exists(os.path.join(courses_dir, course_instance)):
            raise BadRequest(f"Course instance '{course_instance}' does not exist in the courses directory.")

        event = data.get('event')

        if not course_instance or not event:
            raise BadRequest("Both 'course_instance' and 'event' fields are required.")

        valid_events = ["course_update_event", "results_create_event", "results_update_event"]

        # Check if the provided event is valid
        if event not in valid_events:
            raise BadRequest(f"Invalid event type '{event}'. Valid events are: {', '.join(valid_events)}.")

        run_in_background(course_instance, event)

        # Return a success response
        return jsonify({"status": f"Runner Task started {event} on course instance {course_instance}"})

    except BadRequest as e:
        # Handle client-side errors (bad input) and return a 400 error
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        # Handle unexpected server-side errors and return a 500 error
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500


@main_bp.route("/course_event/nifi", methods=['POST'])
def course_event_nifi():
    # Controleer of een geldig token is meegegeven
    auth_token = request.headers.get('Authorization')  # Token in header
    if not auth_token or auth_token != f"Bearer {NIFI_AUTH_TOKEN}":
        return jsonify({'status': 'Error', 'message': 'Unauthorized access'}), 401

    try:
        # Extract JSON data from the request
        data = request.get_json()

        # Check if the JSON data is valid and not empty
        if not data:
            raise BadRequest("Invalid JSON data provided.")

        # Define the absolute path to the 'courses' directory
        courses_dir = os.path.abspath(os.path.join(os.getcwd(), "courses"))

        # Retrieve the 'course_instance' from the JSON data
        course_instance = data.get('course_instance')

        # Check if the specified course_instance exists in the 'courses' directory
        if not os.path.exists(os.path.join(courses_dir, course_instance)):
            raise BadRequest(f"Course instance '{course_instance}' does not exist in the courses directory.")

        # Retrieve the 'event' type from the JSON data
        event = data.get('event')

        # Ensure both 'course_instance' and 'event' fields are present
        if not course_instance or not event:
            raise BadRequest("Both 'course_instance' and 'event' fields are required.")

        # Define the list of valid event types
        valid_events = ["course_update_event", "results_create_event", "results_update_event"]

        # Check if the provided event is valid
        if event not in valid_events:
            raise BadRequest(f"Invalid event type '{event}'. Valid events are: {', '.join(valid_events)}.")

        run_in_background(course_instance, event)


        # Return a success response
        return jsonify({"status": f"Runner Task started {event} on course instance {course_instance}"})

    except BadRequest as e:
        # Handle client-side errors (bad input) and return a 400 error
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        # Handle unexpected server-side errors and return a 500 error
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500


@main_bp.route("/generate/logout", methods=['GET'])
def generate_logout():
    session.pop('admin_authenticated', None)
    return redirect(url_for('main.generate_login'))


@main_bp.route("/")
def auth():
    token = session.get('token', {}).get('access_token')
    if not token:
        return redirect('/auth/login')
    try:
        roles = jwt.decode(token, options={"verify_signature": False}).get("realm_access", {}).get("roles", [])
        if "students" in roles or "teachers" in roles:
            return redirect(url_for('main.select_course'))
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    except jwt.InvalidTokenError:
        return redirect('/auth/login')


@main_bp.route('/dashboard', methods=['GET'])
def dashboard():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Missing authorization header'}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        roles = decoded_token.get("realm_access", {}).get("roles", [])

        # Check of de gebruiker student of leraar is
        if "students" in roles:
            return jsonify({"role": "student"})
        elif "teachers" in roles:
            return jsonify({"role": "teacher"})
        else:
            return jsonify({"message": "Access denied: user has no valid role"}), 403
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Session expired, please login again'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


@main_bp.route('/select_course')
@login_required
def select_course():
    token = session.get('token', {}).get('access_token')
    roles = jwt.decode(token, options={"verify_signature": False}).get("realm_access", {}).get("roles", [])
    if "students" in roles:
        student_courses = session.get('student_courses', [])
        return render_template('select_course/index.html', courses=student_courses)
    elif "teachers" in roles:
        teacher_courses = session.get('teacher_courses', [])
        return render_template('select_course/index.html', courses=teacher_courses)


@main_bp.route('/set_course/<int:course_id>')
@login_required
def set_course(course_id):
    session['selected_course_id'] = course_id
    token = session.get('token', {}).get('access_token')
    roles = jwt.decode(token, options={"verify_signature": False}).get("realm_access", {}).get("roles", [])
    if "students" in roles:
        return redirect(url_for('main.student_dashboard', course_id=course_id))
    if "teachers" in roles:
        return redirect(url_for('main.teacher_dashboard'))


@main_bp.route('/teacher_dashboard')
@login_required
@role_required('teachers')
def teacher_dashboard():
    if os.getenv('STORAGE_TYPE') == 'local':
        matches = glob.glob('/src/courses/*/*/.html')
        matches = glob.glob('/src/courses/*/*/index.html')
        if not matches:
            return jsonify({'message': 'No HTML files found in courses directory'}), 404
            return jsonify({'message': 'No index.html files found in courses directory'}), 404
        directory = os.path.dirname(matches[0])
        return send_from_directory(directory, 'index.html')
    else:
        teacher_index = find_teacher_index()
        if teacher_index:
            return render_template_string(teacher_index)
        else:
            return jsonify({'message': 'No teacher index found'}), 404


@main_bp.route('/student_dashboard/<int:course_id>')
@login_required
@role_required('students')
def student_dashboard(course_id):
    email = jwt.decode(session['token']['access_token'], options={"verify_signature": False}).get("email", "Student")
    stud_dashboard = find_dashboard_by_student_name(email, course_id)
    if stud_dashboard:

        if os.getenv('STORAGE_TYPE') == 'local':
            return render_template_string(open(stud_dashboard).read())

        return render_template_string(stud_dashboard)
    else:
        return jsonify({'message': 'No dashboard found for the selected course'}), 404


@main_bp.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)


@main_bp.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

