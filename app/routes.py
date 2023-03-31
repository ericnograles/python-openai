from flask import Blueprint, jsonify, request
from .auth import jwt_required, role_required

bp = Blueprint('api', __name__)

@bp.route('/v1/user', methods=['GET'])
@jwt_required
@role_required(['Owner', 'Manager', 'Viewer'])
def get_user():
    return jsonify({"message": "Get user"})

@bp.route('/v1/user', methods=['PUT'])
@jwt_required
@role_required(['Owner', 'Manager'])
def update_user():
    return jsonify({"message": "Update user"})

@bp.route('/v1/transformation', methods=['POST'])
@jwt_required
@role_required(['Owner', 'Manager'])
def create_transformation():
    return jsonify({"message": "Create transformation"})

@bp.route('/v1/transformation/<uuid>', methods=['GET'])
@jwt_required
@role_required(['Owner', 'Manager', 'Viewer'])
def get_transformation(uuid):
    return jsonify({"message": f"Get transformation {uuid}"})
