import jwt
import requests
from flask import Blueprint, session, redirect, url_for, request, jsonify
from functools import wraps
from azure_ad_config import AZURE_AD_CONFIG
from src.db.course_data import get_student_courses, get_teacher_courses
from src.db.db_context import db_context

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def azure_ad_login():
    """Redirect to Azure AD for login."""
    auth_url = f"{AZURE_AD_CONFIG['AUTHORITY']}/oauth2/v2.0/authorize"
    params = {
        'client_id': AZURE_AD_CONFIG['CLIENT_ID'],
        'response_type': 'code',
        'redirect_uri': AZURE_AD_CONFIG['REDIRECT_URI'],
        'response_mode': 'query',
        'scope': ' '.join(AZURE_AD_CONFIG['SCOPE'])
    }
    url = requests.Request('GET', auth_url, params=params).prepare().url
    return redirect(url)

@auth_bp.route('/login/callback')
def azure_ad_callback():
    """Handle the Azure AD callback and authenticate the user."""
    code = request.args.get('code')
    if not code:
        print("Debug: No authorization code found in the request.")
        return jsonify({'message': 'Authorization code not found'}), 400

    # Exchange code for tokens
    token_url = f"{AZURE_AD_CONFIG['AUTHORITY']}/oauth2/v2.0/token"
    data = {
        'client_id': AZURE_AD_CONFIG['CLIENT_ID'],
        'scope': ' '.join(AZURE_AD_CONFIG['SCOPE']),
        'code': code,
        'redirect_uri': AZURE_AD_CONFIG['REDIRECT_URI'],
        'grant_type': 'authorization_code',
        'client_secret': AZURE_AD_CONFIG['CLIENT_SECRET']
    }

    try:
        response = requests.post(token_url, data=data)
        print(f"Debug: Token response status code: {response.status_code}")
        print(f"Debug: Token response body: {response.text}")

        response.raise_for_status()
        tokens = response.json()
        access_token = tokens.get('access_token')

        if not access_token:
            print("Debug: No access token found in the response.")
            return jsonify({'message': 'Access token not found in response'}), 400

        # Decode the token to get user email
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        print(f"Debug: Decoded token: {decoded_token}")

        # Check for different possible email claims
        user_email = (
            decoded_token.get('preferred_username') or
            decoded_token.get('email') or
            decoded_token.get('upn')  # UPN (User Principal Name) might be used instead of email
        )

        print(f"Debug: Extracted email: {user_email}")

        if not user_email:
            return jsonify({'message': 'Email not found in token'}), 400

        session['token'] = tokens
        session['email'] = user_email

        # Check if user is a student or teacher
        with db_context() as (cursor, connection):
            cursor.execute("SELECT * FROM students WHERE email = %s", (user_email,))
            student = cursor.fetchone()
            print(f"Debug: Student lookup result: {student}")

            cursor.execute("SELECT * FROM teachers WHERE email = %s", (user_email,))
            teacher = cursor.fetchone()
            print(f"Debug: Teacher lookup result: {teacher}")

            if student:
                session['role'] = 'student'
                session['student_courses'] = get_student_courses(user_email)
                return redirect(url_for('main.select_course'))
            elif teacher:
                session['role'] = 'teacher'
                session['teacher_courses'] = get_teacher_courses(user_email)
                return redirect(url_for('main.select_course'))
            else:
                print("Debug: User not found in the database.")
                return jsonify({'message': 'User not found in database'}), 403

    except requests.exceptions.RequestException as e:
        print(f"Debug: Token exchange request failed: {e}")
        return jsonify({'message': f'Token exchange failed: {e}'}), 500
    except Exception as e:
        print(f"Debug: General error: {e}")
        return jsonify({'message': f'Login failed: {e}'}), 500

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('auth.azure_ad_login'))
        return f(*args, **kwargs)

    return decorated_function

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            roles = get_user_roles()
            print(f"Checking for role '{role}' in roles: {roles}")
            if role not in roles:
                print("Access denied: role not found")
                return jsonify({'message': 'Forbidden - Access denied'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.azure_ad_login'))

def get_user_roles():
    session_roles = session.get('roles')
    if session_roles:
        print(f"Roles from session: {session_roles}")
        return session_roles

    token = session.get('token', {}).get('access_token')
    if not token:
        return []

    decoded_token = jwt.decode(token, options={"verify_signature": False})
    roles = decoded_token.get("realm_access", {}).get("roles", [])
    print(f"Roles from token: {roles}")
    return roles
