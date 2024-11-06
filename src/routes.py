import glob
import os
from flask import Blueprint, jsonify, redirect, session, send_from_directory, request, render_template_string
from src.auth import login_required, role_required
import jwt
from db import utils

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def main():
    token = session.get('token', {}).get('access_token')
    if not token:
        return redirect('/auth/login')
    try:
        roles = jwt.decode(token, options={"verify_signature": False}).get("realm_access", {}).get("roles", [])
        return redirect('/teacher_dashboard' if "teachers" in roles else '/student_dashboard') if roles else jsonify(
            {'message': 'Unauthorized'}), 403
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


@main_bp.route('/teacher_dashboard')
@login_required
@role_required('teachers')
def teacher_dashboard():
    matches = glob.glob('/src/courses/*/*/.html')
    if not matches:
        return jsonify({'message': 'No HTML files found in courses directory'}), 404
    directory = os.path.dirname(matches[0])
    return send_from_directory(directory, 'index.html')


@main_bp.route('/student_dashboard')
@login_required
@role_required('students')
def student_dashboard():
    email = jwt.decode(session['token']['access_token'], options={"verify_signature": False}).get("email", "Student")
    stud_dashboard = utils.find_dashboard_by_student_name(email)
    if stud_dashboard:
        return render_template_string(open(stud_dashboard).read())
    else:
        return jsonify({'message': 'No dashboard found for the student'}), 404

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
    stud_dashboard = utils.find_dashboard_by_student_name(student_email)

    if stud_dashboard:
        return render_template_string(open(stud_dashboard).read())
    else:
        return jsonify({'message': 'No dashboard found for the student'}), 404
