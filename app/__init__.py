from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

# Initialize extensions
login_manager = LoginManager()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    # Enable CORS for frontend with credentials support
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

    from . import models  # Ensure models are registered
    from .routes import auth_bp
    from .jobs import jobs_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')

    # Custom error handlers
    @app.errorhandler(400)
    def bad_request(e):
        return {'error': 'Bad Request'}, 400

    @app.errorhandler(401)
    def unauthorized(e):
        return {'error': 'Unauthorized'}, 401

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not Found'}, 404

    @app.errorhandler(500)
    def internal_error(e):
        return {'error': 'Internal Server Error'}, 500

    return app 