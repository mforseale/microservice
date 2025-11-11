from flask import Blueprint, request, jsonify
from .models import User
from .utils.logger import setup_logger

logger = setup_logger()
bp = Blueprint('api', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Service is running'})

@bp.route('/users', methods=['GET'])
def get_users():
    """GET all users"""
    try:
        users = User.get_all()
        return jsonify([dict(user) for user in users])
    except Exception as e:
        logger.error(f"Error in GET /users: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """GET user by ID"""
    try:
        user = User.get_by_id(user_id)
        if user:
            return jsonify(dict(user))
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error in GET /users/{user_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users', methods=['POST'])
def create_user():
    """POST create new user"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400
        
        name = data['name']
        email = data['email']
        
        if not isinstance(name, str) or not isinstance(email, str):
            return jsonify({'error': 'Name and email must be strings'}), 400
        
        if len(name.strip()) == 0 or len(email.strip()) == 0:
            return jsonify({'error': 'Name and email cannot be empty'}), 400
        
        user = User.create(name, email)
        return jsonify(dict(user)), 201
        
    except Exception as e:
        logger.error(f"Error in POST /users: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """PUT update user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        email = data.get('email')
        
        if name is not None and (not isinstance(name, str) or len(name.strip()) == 0):
            return jsonify({'error': 'Name must be a non-empty string'}), 400
        
        if email is not None and (not isinstance(email, str) or len(email.strip()) == 0):
            return jsonify({'error': 'Email must be a non-empty string'}), 400
        
        user = User.update(user_id, name, email)
        
        if user:
            return jsonify(dict(user))
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        logger.error(f"Error in PUT /users/{user_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """DELETE user"""
    try:
        user = User.delete(user_id)
        
        if user:
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        logger.error(f"Error in DELETE /users/{user_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405