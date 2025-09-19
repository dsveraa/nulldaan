from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


debug_bp = Blueprint('debug', __name__)


@debug_bp.route('/check-session')
@jwt_required()
def check_session():
    current_user = get_jwt_identity()
    return jsonify({'status': 'ok', 'user': current_user}), 200


@debug_bp.route('/protected', methods=['POST'])
@jwt_required()
def protected():
    data = request.get_json()
    name = data.get('name')

    return jsonify({'status': 'ok', 'name': f'{name} from backend'}), 200


@debug_bp.route('/unprotected/<name>')
def unprotected(name):    
    return jsonify({'status': 'ok', 'name': name}), 200


@debug_bp.route('/')
def is_running():
    return jsonify({'status': 'ok'}), 200


@debug_bp.route("/ping", methods=["GET", "OPTIONS"])
def ping():
    return {"pong": True}
