from flask import Blueprint, jsonify, request
from .auth import jwt_required, role_required
from .controllers.user_controller import get_user, update_user
from .controllers.transformation_controller import create_transformation, get_transformation

bp = Blueprint('api', __name__)

@bp.route('/v1/user', methods=['GET'])
@jwt_required
@role_required(['Owner', 'Manager', 'Viewer'])
def get_user_route():
    return jsonify(get_user())

@bp.route('/v1/user', methods=['PUT'])
@jwt_required
@role_required(['Owner', 'Manager'])
def update_user_route():
    return jsonify(update_user())

@bp.route('/v1/transformation', methods=['POST'])
@jwt_required
@role_required(['Owner', 'Manager'])
def create_transformation_route():
    return jsonify(create_transformation())

@bp.route('/v1/transformation/<uuid>', methods=['GET'])
@jwt_required
@role_required(['Owner', 'Manager', 'Viewer'])
def get_transformation_route(uuid):
    return jsonify(get_transformation(uuid))
