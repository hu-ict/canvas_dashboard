from flask import Flask

from src.auth import auth_bp
from src.routes import main_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_random_generated_secret_key'  # Change This
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5101)
