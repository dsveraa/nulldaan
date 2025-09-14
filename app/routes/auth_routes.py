from flask import request, jsonify, Blueprint

from app.services.auth_services import Logout, UserAuth, UserRegistration


auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user_auth = UserAuth(email, password)
    authorized = user_auth.auth()
    username = user_auth.get_username()

    if authorized:
        return jsonify({"status": "ok", "username": username }), 200
    else:
        return jsonify ({"status": "error"}), 401


@auth_bp.route("/logout")
def logout():
    logout_query = Logout()
    return jsonify({ "response": logout_query })


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    registration = UserRegistration(name, email, password)
    result = registration.register()

    if result['status'] == 'error':
        return jsonify(result), 400

    return jsonify(result)
