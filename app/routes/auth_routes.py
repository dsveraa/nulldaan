from flask import request, jsonify, Blueprint
from app.services.auth_services import Logout, AccountManagement, SignUp


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    account = AccountManagement(email, password)
    authorized = account.login()
    username = account.get_username()

    if authorized:
        return jsonify({'status': 'ok', 'username': username}), 200
    else:
        return jsonify ({'status': 'error'}), 401


@auth_bp.route('/logout')
def logout():
    logout_query = Logout()
    return jsonify({'response': logout_query}), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    signup = SignUp(name, email, password)
    result = signup.signup()

    if result['status'] == 'error':
        return jsonify(result), 400

    return jsonify(result), 201


@auth_bp.route('/account/<email>', methods=['DELETE'])
def delete_account(email):
    account = AccountManagement(email)
    account.delete_user()    
    return 'deleted', 204
