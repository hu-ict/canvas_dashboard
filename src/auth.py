# src/auth.py
from functools import wraps

import jwt
from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for
from keycloak.exceptions import KeycloakAuthenticationError

from keycloak_config import keycloak_openid
from src.db.course_data import get_student_courses, get_teacher_courses

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        token = keycloak_openid.token(username, password)
        session['token'] = token

        if username.endswith("@student.hu.nl"):
            # Get courses for the student and store them in session
            student_courses = get_student_courses(username)
            session['student_courses'] = student_courses
        if username.endswith("@hu.nl"):
            # Get courses for the teacher and store them in session
            teacher_courses = get_teacher_courses(username)
            session['teacher_courses'] = teacher_courses

        return jsonify({
            'message': 'Login successful',
            'access_token': token['access_token'],
            'refresh_token': token.get('refresh_token'),
            'id_token': token.get('id_token')
        }), 200
    except KeycloakAuthenticationError:
        return jsonify({'message': 'Invalid username or password'}), 401


@auth_bp.route('/login')
def login_page():
    return render_template('login/index.html')


def get_user_roles():
    token = session.get('token', {}).get('access_token')
    if not token:
        return []
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    return decoded_token.get("realm_access", {}).get("roles", [])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('token', {}).get('access_token')
        if not token:
            print("Login required: no token found.")
            return jsonify({'message': 'Login required'}), 401
        try:
            keycloak_openid.userinfo(token)
        except KeycloakAuthenticationError:
            print("Invalid token: token verification failed.")
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)

    return decorated_function


def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            roles = get_user_roles()
            if role not in roles:
                return jsonify({'message': 'Forbidden - Access denied'}), 403
            return f(*args, **kwargs)

        return decorated_function

    return wrapper


@auth_bp.route('/logout')
def logout():
    # Clear session data
    session.pop('token', None)
    session.pop('student_courses', None)
    session.pop('selected_course_id', None)

    # Redirect to login
    return redirect(url_for('auth.login_page'))
