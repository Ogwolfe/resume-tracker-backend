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
    CORS(app)

    from . import models  # Ensure models are registered
    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    return app 