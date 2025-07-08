from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400
    try:
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return jsonify({'error': 'User already exists'}), 400
        hashed_pw = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    try:
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return jsonify({'message': 'Logged in successfully'})
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500

@auth_bp.route('/api/me', methods=['GET'])
@login_required
def get_current_user():
    user = current_user
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }) 