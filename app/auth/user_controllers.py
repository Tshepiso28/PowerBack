from app.auth.user_models import User
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

bcrypt = Bcrypt()
blacklist = set()

def token_in_blocklist_loader(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blacklist

def signup():
    data = request.get_json()
    name, email, password = data.get('full_name'), data.get('email'), data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    if User.find_by_email(email):
        return jsonify({'message': 'User already exists'}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    User.create_user(name, email, password_hash)

    return jsonify({'message': 'User created successfully'}), 201

def signin():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400
    
    user = User.find_by_email(email)
    if user and bcrypt.check_password_hash(user['password_hash'], password):
        access_token = create_access_token(identity=str(user['id']))
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@jwt_required()
def signout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({'message': 'Successfully signed out'}), 200