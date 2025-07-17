import pytest
from app import create_app, db
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    app.config.update({"LOGIN_DISABLED": False})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def logged_in_client(app):
    client = app.test_client()
    client.post("/register", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "pw456"
    })
    client.post("/login", json={
        "username": "bob",
        "password": "pw456"
    })
    return client

def test_register_success(client):
    resp = client.post("/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "pw123"
    })
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "User registered successfully"

def test_register_duplicate(client):
    client.post("/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "pw123"
    })
    resp = client.post("/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "pw123"
    })
    assert resp.status_code == 400
    assert "error" in resp.get_json()

def test_register_missing_fields(client):
    resp = client.post("/register", json={"username": "alice"})
    assert resp.status_code == 400
    assert "error" in resp.get_json()

def test_login_success(client):
    client.post("/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "pw123"
    })
    resp = client.post("/login", json={
        "username": "alice",
        "password": "pw123"
    })
    assert resp.status_code == 200
    assert "Logged in successfully" in resp.get_json()["message"]

def test_login_invalid(client):
    resp = client.post("/login", json={
        "username": "notfound",
        "password": "wrong"
    })
    assert resp.status_code == 401
    assert "error" in resp.get_json()

def test_me_authenticated(logged_in_client):
    resp = logged_in_client.get("/api/me")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["username"] == "bob"
    assert data["email"] == "bob@example.com"

def test_me_unauthenticated(client):
    resp = client.get("/api/me")
    assert resp.status_code == 401

def test_logout(logged_in_client):
    resp = logged_in_client.post("/logout")
    assert resp.status_code == 200
    assert "Logged out successfully" in resp.get_json()["message"]

def test_session_invalidated_after_logout(logged_in_client):
    # Logout
    resp = logged_in_client.post("/logout")
    assert resp.status_code == 200
    # Try to access an authenticated endpoint
    resp = logged_in_client.get("/api/me")
    assert resp.status_code == 401
    # Try to access jobs endpoint
    resp = logged_in_client.get("/api/jobs/")
    assert resp.status_code == 401

def test_jobs_crud(logged_in_client):
    job_data = {
        "company": "Acme Corp",
        "position": "Engineer",
        "resume_used": "resume.pdf",
        "date_applied": "2024-01-01",
        "status": "applied"
    }
    # Create
    resp = logged_in_client.post("/api/jobs/", json=job_data)
    assert resp.status_code == 201
    job_id = resp.get_json()["id"]
    # Read
    resp = logged_in_client.get("/api/jobs/")
    assert resp.status_code == 200
    jobs = resp.get_json()
    assert len(jobs) == 1
    assert jobs[0]["company"] == "Acme Corp"
    # Update
    update_data = {"status": "interview"}
    resp = logged_in_client.put(f"/api/jobs/{job_id}", json=update_data)
    assert resp.status_code == 200
    # Confirm update
    resp = logged_in_client.get("/api/jobs/")
    jobs = resp.get_json()
    assert jobs[0]["status"] == "interview"
    # Delete
    resp = logged_in_client.delete(f"/api/jobs/{job_id}")
    assert resp.status_code == 200
    # Confirm delete
    resp = logged_in_client.get("/api/jobs/")
    assert resp.get_json() == []
    # Unauthenticated client
    from app import create_app, db
    from config import TestingConfig
    new_app = create_app(TestingConfig)
    with new_app.app_context():
        db.create_all()
        unauth_client = new_app.test_client()
        resp = unauth_client.get("/api/jobs/")
        assert resp.status_code == 401
        resp = unauth_client.post("/api/jobs/", json=job_data)
        assert resp.status_code == 401

def test_jobs_create_missing_field(logged_in_client):
    # Missing required field 'company'
    job_data = {
        "position": "Engineer",
        "resume_used": "resume.pdf",
        "date_applied": "2024-01-01",
        "status": "applied"
    }
    resp = logged_in_client.post("/api/jobs/", json=job_data)
    assert resp.status_code == 400
    assert "error" in resp.get_json()

def test_jobs_update_not_found(logged_in_client):
    # Try to update a non-existent job
    update_data = {"status": "interview"}
    resp = logged_in_client.put("/api/jobs/999", json=update_data)
    assert resp.status_code == 404
    assert "error" in resp.get_json()

def test_jobs_delete_not_found(logged_in_client):
    # Try to delete a non-existent job
    resp = logged_in_client.delete("/api/jobs/999")
    assert resp.status_code == 404
    assert "error" in resp.get_json()

def test_cors_headers(client):
    # Allowed origin (should echo the origin)
    resp = client.options(
        "/api/jobs/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST"
        }
    )
    assert resp.status_code == 200
    assert resp.headers.get("Access-Control-Allow-Origin") == "http://localhost:5173"
    assert resp.headers.get("Access-Control-Allow-Credentials") == "true"

def test_cors_blocks_disallowed_origin():
    # Create a new app with a specific allowed origin
    from app import create_app, db
    from config import TestingConfig

    class CustomConfig(TestingConfig):
        FRONTEND_ORIGIN = "http://allowed-origin.com"

    app = create_app(CustomConfig)
    with app.app_context():
        db.create_all()
        test_client = app.test_client()
        # Allowed origin
        resp = test_client.options(
            "/api/jobs/",
            headers={
                "Origin": "http://allowed-origin.com",
                "Access-Control-Request-Method": "POST"
            }
        )
        assert resp.status_code == 200
        assert resp.headers.get("Access-Control-Allow-Origin") == "http://allowed-origin.com"
        # Disallowed origin
        resp = test_client.options(
            "/api/jobs/",
            headers={
                "Origin": "http://disallowed.com",
                "Access-Control-Request-Method": "POST"
            }
        )
        # Should not include CORS headers for disallowed origin
        assert resp.headers.get("Access-Control-Allow-Origin") is None
