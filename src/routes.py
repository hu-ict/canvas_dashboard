import glob
import os
from flask import Blueprint, jsonify, redirect, session, send_from_directory, request, render_template_string, \
    render_template, url_for
from src.auth import login_required, role_required
import jwt
from generate_start import main_generate
from runner import main as runner
from src.db.generate_data import initialize_db

from src.db.dashboards import find_dashboard_by_student_name

main_bp = Blueprint('main', __name__)

@main_bp.route("/generate/start", methods=['POST'])
def generate_start():

    data = request.get_json()

    print(data)
    try:
        main_generate(data['new_instance'], data['category'], data['canvas_course_id'], data['canvas_api_key'])
    except Exception as e:
        print(f"An error occurred while generating the start file: {e}")
        return jsonify({'message': 'An error occurred while generating the start file'}), 500

    print("Event emitted")
    runner(data['new_instance'], "course_create_event")

    initialize_db()

    return data

@main_bp.route("/")
def auth():
    token = session.get('token', {}).get('access_token')
    if not token:
        return redirect('/auth/login')
    try:
        roles = jwt.decode(token, options={"verify_signature": False}).get("realm_access", {}).get("roles", [])
        if "students" in roles:
            return redirect(url_for('main.select_course'))
        elif "teachers" in roles:
            return redirect(url_for('main.teacher_dashboard'))
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
@role_required('students')
def select_course():
    # Get the student courses from the session
    student_courses = session.get('student_courses', [])

    # Render the select course page with the student courses
    return render_template('select_course/index.html', courses=student_courses)


@main_bp.route('/set_course/<int:course_id>')
@login_required
@role_required('students')
def set_course(course_id):
    session['selected_course_id'] = course_id
    return redirect(url_for('main.student_dashboard', course_id=course_id))



@main_bp.route('/teacher_dashboard')
@login_required
@role_required('teachers')
def teacher_dashboard():
    matches = glob.glob('/src/courses/*/*/.html')
    if not matches:
        return jsonify({'message': 'No HTML files found in courses directory'}), 404
    directory = os.path.dirname(matches[0])
    return send_from_directory(directory, 'index.html')


@main_bp.route('/student_dashboard/<int:course_id>')
@login_required
@role_required('students')
def student_dashboard(course_id):
    email = jwt.decode(session['token']['access_token'], options={"verify_signature": False}).get("email", "Student")
    stud_dashboard = find_dashboard_by_student_name(email, course_id)
    if stud_dashboard:
        return render_template_string(open(stud_dashboard).read())
    else:
        return jsonify({'message': 'No dashboard found for the selected course'}), 404



@main_bp.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)


@main_bp.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)


@main_bp.route('/student_dashboard/hardcoded')
@login_required
def dashboard_jeroen():
    student_email = "jeroen.cabri@student.hu.nl"
    stud_dashboard = find_dashboard_by_student_name(student_email)

    if stud_dashboard:
        return render_template_string(open(stud_dashboard).read())
    else:
        return jsonify({'message': 'No dashboard found for the student'}), 404
