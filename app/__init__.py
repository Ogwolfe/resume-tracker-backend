from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import DevelopmentConfig, ProductionConfig, TestingConfig
import os

# Initialize extensions
login_manager = LoginManager()
db = SQLAlchemy()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is not None:
        app.config.from_object(config_class)
        print(f"Running with custom config: {config_class.__name__}")
    else:
        # Load configuration based on environment
        # Use FLASK_DEBUG for modern Flask versions (FLASK_ENV is deprecated)
        flask_debug = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
        flask_env = os.getenv("FLASK_ENV", "development").lower()
        
        if flask_env == "production" or (not flask_debug and flask_env != "development"):
            app.config.from_object(ProductionConfig)
            print("Running in PRODUCTION mode")
        elif flask_env == "testing":
            app.config.from_object(TestingConfig)
            print("Running in TESTING mode")
        else:
            app.config.from_object(DevelopmentConfig)
            print("Running in DEVELOPMENT mode")

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = None  # disables redirect to login page


    # Get frontend origin from config
    frontend_origin = app.config.get("FRONTEND_ORIGIN", app.config.get("CORS_ORIGINS", "*"))
    CORS(app, resources={r"/*": {"origins": frontend_origin}}, supports_credentials=True)


    # Import models and blueprints
    from . import models
    from .routes import auth_bp
    from .jobs import jobs_bp

    # Register blueprints (CORS will apply globally via app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')

    # Error handlers
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

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return {'error': 'Unauthorized'}, 401

    return app

