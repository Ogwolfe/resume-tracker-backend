import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class with common settings"""
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_dev_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
    
    # Common settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    
    # Development-specific settings
    SQLALCHEMY_ECHO = True  # Log SQL queries
    JSONIFY_PRETTYPRINT_REGULAR = True  # Pretty print JSON responses
    
    # Development CORS settings
    FRONTEND_ORIGIN = "http://localhost:5173"

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    SQLALCHEMY_ECHO = False
    
    # Production CORS settings
    FRONTEND_ORIGIN = "https://resume-tracker-frontend.onrender.com"
    
    # Additional production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"

class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    
    # Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    # Testing-specific settings
    WTF_CSRF_ENABLED = False
