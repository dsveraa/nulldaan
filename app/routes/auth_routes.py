from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.repositories.user_repository import UserRepository
from app.services.auth_services import AuthService
from app.services.user_services import SignUpService


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        user, access_token, refresh_token = AuthService.login(email, password)
        return jsonify({
            'status': 'ok', 
            'user': {
                'id': user.id,
                'name': user.name                            
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    
    except ValueError as e: 
        return jsonify({'status': 'error', 'message': str(e)}), 401


@auth_bp.route('/logout')
def logout():
    logout_query = AuthService.logout()
    return jsonify({'response': logout_query}), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    try:
        new_user = SignUpService.register(name, email, password)
        return jsonify({"status": "ok",
            "user_id": new_user.id,
            "name": new_user.name
        }), 201

    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


@auth_bp.route('/account/<email>', methods=['DELETE']) # development
def delete_account(email):
    user = UserRepository.get_by_email(email)
    UserRepository.delete(user)
    return 'deleted', 204


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": new_access_token})
