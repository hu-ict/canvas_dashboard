import glob
import os
from functools import wraps

from flask import Flask, send_from_directory, request, redirect, session, jsonify, make_response
from keycloak.exceptions import KeycloakAuthenticationError

from keycloak_config import keycloak_openid

app = Flask(__name__)
app.secret_key = 'your_random_generated_secret_key' # Change this!


# Teacher Dashboard
@app.route("/")
def main():
    # Controleer of de gebruiker is ingelogd
    token = session.get('token', {}).get('access_token')
    if not token:
        return redirect('/login')  # Gebruiker is niet ingelogd, dus redirect naar de loginpagina

    try:
        # Verifieer het token om te controleren of de sessie geldig is
        user_info = keycloak_openid.userinfo(token)
        request.user = user_info
    except KeycloakAuthenticationError:
        return redirect('/login')  # Token is ongeldig, dus redirect naar de loginpagina

    # Gebruiker is ingelogd en token is geldig, dus doorverwijzen naar /protected
    return redirect('/protected')


@app.route("/<path:filename>")
def main_serve(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    # Print the directories
    for directory in directories_list:
        print(directory)
    return send_from_directory(directories_list[0], filename)


# Route to serve CSS, JS, and other static files from 'vendor' directory
@app.route('/vendor/<path:filename>')
def serve_vendor(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    path_parts = request.path.split('/')

    # Remove the last part (the filename or last directory)
    filez = path_parts.pop()  # Removes the last element from the list

    # Join the parts back into a path
    new_path = '/'.join(path_parts)

    print(f"Full URL Path: {directories_list[0] + new_path} - {filez}")
    return send_from_directory(directories_list[0] + new_path, filez)


# Route to serve CSS files
@app.route('/css/<path:filename>')
def serve_css(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    path_parts = request.path.split('/')

    # Remove the last part (the filename or last directory)
    filez = path_parts.pop()  # Removes the last element from the list

    # Join the parts back into a path
    new_path = '/'.join(path_parts)

    print(f"Full URL Path: {directories_list[0] + new_path} - {filez}")
    return send_from_directory(directories_list[0] + new_path, filez)


# Route to serve JS files
@app.route('/js/<path:filename>')
def serve_js(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    path_parts = request.path.split('/')

    # Remove the last part (the filename or last directory)
    filez = path_parts.pop()  # Removes the last element from the list

    # Join the parts back into a path
    new_path = '/'.join(path_parts)

    print(f"Full URL Path: {directories_list[0] + new_path} - {filez}")
    return send_from_directory(directories_list[0] + new_path, filez)
@app.route('/plotly/<path:filename>')
def serve_plotly(filename):
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    path_parts = request.path.split('/')

    # Remove the last part (the filename or last directory)
    filez = path_parts.pop()  # Removes the last element from the list

    # Join the parts back into a path
    new_path = '/'.join(path_parts)

    print(f"Full URL Path: {directories_list[0] + new_path} - {filez}")
    return send_from_directory(directories_list[0] + new_path, filez)

# Acces to images an css for login page
@app.route('/login/<path:filename>')
def serve_login_files(filename):
    return send_from_directory('login', filename)

@app.route('/login/images/<path:filename>')
def serve_login_images(filename):
    return send_from_directory('login/images', filename)

@app.route('/login/js/<path:filename>')
def serve_login_js(filename):
    return send_from_directory('login/js', filename)



# Login Requests

# Login html

@app.route("/login")
def login_page():
    return send_from_directory('login', 'index.html')

# Login postman
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        # Vraag een token aan bij Keycloak met de inloggegevens
        token = keycloak_openid.token(username, password)

        # Zet de token in de sessie (optioneel, alleen als je server-side sessies wilt gebruiken)
        session['token'] = token

        # Stuur de tokens terug naar de frontend
        return jsonify({
            'message': 'Login successful',
            'access_token': token['access_token'],
            'refresh_token': token.get('refresh_token'),
            'id_token': token.get('id_token')
        }), 200

    except KeycloakAuthenticationError:
        # Fout bij authenticatie, stuur een foutmelding terug
        return jsonify({'message': 'Invalid username or password'}), 401

# security check
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('token', {}).get('access_token')
        if not token:
            return jsonify({'message': 'Login required'}), 401
        try:
            # Verifieer het token met Keycloak
            user_info = keycloak_openid.userinfo(token)
            request.user = user_info
        except KeycloakAuthenticationError:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated_function

# protected route
@app.route('/protected')
@login_required
def protected():
    # Use glob to find all HTML files matching the pattern
    matches = glob.glob('./courses/*/*/*.html')

    # Get unique directories that contain the HTML files
    directories = set(os.path.dirname(match) for match in matches)
    directories_list = list(directories)
    # Print the directories
    for directory in directories_list:
        print(directory)
    return send_from_directory(directories_list[0], 'index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5101)

