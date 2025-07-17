# Flask Application Configuration

This Flask application supports multiple environments (development, production, testing) with different configurations.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

### Required Variables
- `SECRET_KEY`: Secret key for session management and security
- `SQLALCHEMY_DATABASE_URI`: Database connection string

### Environment Control
- `FLASK_ENV`: Set to "development", "production", or "testing"
- `FLASK_DEBUG`: Set to "1", "true", or "yes" for development mode

### Optional Variables
- `SESSION_COOKIE_SECURE`: Set to "true" for HTTPS-only cookies (production)
- `SESSION_COOKIE_SAMESITE`: Cookie security policy ("Lax", "Strict", "None")

## Example .env Files

### Development (.env)
```
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=dev-secret-key-change-in-production
SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_SAMESITE=Lax
```

### Production (.env)
```
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-super-secure-production-secret-key
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/production_db
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=Strict
```

### Testing (.env)
```
FLASK_ENV=testing
FLASK_DEBUG=1
SECRET_KEY=test-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///:memory:
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_SAMESITE=Lax
```

## Configuration Classes

The application uses different configuration classes based on the environment:

### DevelopmentConfig
- Debug mode enabled
- SQL query logging enabled
- Pretty JSON responses
- CORS allows localhost:5173

### ProductionConfig
- Debug mode disabled
- Enhanced security settings
- CORS allows production frontend URL
- Secure cookie settings

### TestingConfig
- In-memory SQLite database
- Debug mode enabled
- CSRF protection disabled for testing

## Running the Application

### Development
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

### Production
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### Testing
```bash
export FLASK_ENV=testing
python -m pytest
``` 