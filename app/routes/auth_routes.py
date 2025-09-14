from flask import request, jsonify, Blueprint

from app.services.auth_services import UserAuth


auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    authorized = UserAuth(email, password)

    if authorized:
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify ({"status": "error"}), 401
