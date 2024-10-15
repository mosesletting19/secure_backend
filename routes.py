from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from models import User
from extensions import db, bcrypt

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    data = request.json  # Change from request.form to request.json
    print("Received data:", data)  # Debugging line
    
    full_name = data.get('full_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')
    role = data.get('role')

    print("Password:", password)  # Debugging line

    if User.query.filter_by(email=email).first() or User.query.filter_by(phone_number=phone_number).first():
        return jsonify({'error': 'User with this email or phone number already exists.'}), 400

    if not password:  # Check if the password is empty
        return jsonify({'error': 'Password must not be empty.'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(full_name=full_name, email=email, phone_number=phone_number, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully.'}), 201

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    data = request.json  # Use request.json to get the incoming data
    print("Received login data:", data)  # Debugging line

    phone_number = data.get('phone_number')
    password = data.get('password')

    print("Phone Number:", phone_number)  # Debugging line
    print("Password:", password)  # Debugging line

    # Check if any fields are empty
    if not phone_number or not password:
        return jsonify({'error': 'Phone number and password must not be empty.'}), 400

    user = User.query.filter_by(phone_number=phone_number).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful.', 'role': user.role}), 200  # Send role in response
    
    return jsonify({'error': 'Invalid credentials.'}), 401

@auth_routes.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully.'}), 200
