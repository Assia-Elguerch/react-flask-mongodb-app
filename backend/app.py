from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# JWT Configuration
jwt_secret_key = os.environ.get('JWT_SECRET_KEY')
if not jwt_secret_key:
    raise ValueError("JWT_SECRET_KEY environment variable is required")
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=24)

# Rate Limiting Configuration
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)

# Configuration MongoDB depuis les variables d'environnement
mongodb_host = os.environ.get('MONGODB_HOST', 'mongodb')
mongodb_username = os.environ.get('MONGODB_USERNAME')
mongodb_password = os.environ.get('MONGODB_PASSWORD')
mongodb_database = os.environ.get('MONGODB_DATABASE', 'flaskdb')

if not mongodb_username or not mongodb_password:
    raise ValueError("MONGODB_USERNAME and MONGODB_PASSWORD environment variables are required")

app.config['MONGO_URI'] = f'mongodb://{mongodb_username}:{mongodb_password}@{mongodb_host}:27017/{mongodb_database}?authSource=admin'

mongo = PyMongo(app)

CORS(app)


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Extract token from "Bearer <token>"
                token = auth_header.split(' ')[1] if 'Bearer' in auth_header else auth_header
            except IndexError:
                return jsonify({'message': 'Token is missing'}), 401

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Decode and verify token
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# User Registration Endpoint
@app.route('/api/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    try:
        data = request.get_json()

        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username and password are required'}), 400

        username = data['username']
        password = data['password']

        # Check if user already exists
        users = mongo.db.users
        if users.find_one({'username': username}):
            return jsonify({'message': 'Username already exists'}), 400

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create user
        user_id = users.insert_one({
            'username': username,
            'password': hashed_password.decode('utf-8')
        }).inserted_id

        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user_id),
            'username': username,
            'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
        }, app.config['JWT_SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user_id': str(user_id)
        }), 201

    except Exception as e:
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500


# User Login Endpoint
@app.route('/api/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    try:
        data = request.get_json()

        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username and password are required'}), 400

        username = data['username']
        password = data['password']

        # Find user
        users = mongo.db.users
        user = users.find_one({'username': username})

        if not user:
            return jsonify({'message': 'Invalid username or password'}), 401

        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'message': 'Invalid username or password'}), 401

        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'username': username,
            'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
        }, app.config['JWT_SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user_id': str(user['_id'])
        }), 200

    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500


@app.route('/api/tasks', methods=['GET'])
@limiter.limit("100 per minute")
def get_all_tasks():
    tasks = mongo.db.tasks

    result = []

    for field in tasks.find():
        result.append({'_id': str(field['_id']), 'title': field['title']})
    return jsonify(result)

@app.route('/api/task', methods=['POST'])
@limiter.limit("50 per minute")
def add_task():
    tasks = mongo.db.tasks
    title = request.get_json()['title']

    task_id = tasks.insert_one({'title': title}).inserted_id
    new_task = tasks.find_one({'_id':task_id})

    result = {'title' : new_task['title']}

    return jsonify({'result': result})

@app.route('/api/task/<id>', methods=['PUT'])
@limiter.limit("50 per minute")
@token_required
def update_task(current_user, id):
    tasks = mongo.db.tasks
    title = request.get_json()['title']

    tasks.find_one_and_update({'_id':ObjectId(id)}, {"$set": {"title": title}}, upsert=False)
    new_task = tasks.find_one({'_id': ObjectId(id)})

    result = {'title' : new_task['title']}

    return jsonify({"result": result})

@app.route('/api/task/<id>', methods=['DELETE'])
@limiter.limit("50 per minute")
@token_required
def delete_task(current_user, id):
    tasks = mongo.db.tasks

    response = tasks.delete_one({'_id': ObjectId(id)})

    if response.deleted_count == 1:
        result = {'message' : 'record deleted'}
    else:
        result = {'message' : 'no record found'}

    return jsonify({'result' : result})

if __name__ == '__main__':
    app.run(debug=True)
