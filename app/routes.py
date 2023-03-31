from flask import Blueprint, jsonify
from .auth import jwt_required

bp = Blueprint('api', __name__, url_prefix='/v1')

@bp.route('/user', methods=['GET'])
@jwt_required
def get_user():
    # Add logic to get user
    return jsonify({'message': 'GET /v1/user'})

@bp.route('/user', methods=['PUT'])
def update_user():
    # Add logic to update user
    return jsonify({'message': 'PUT /v1/user'})

@bp.route('/transformation', methods=['POST'])
def create_transformation():
    # Add logic to create a transformation
    return jsonify({'message': 'POST /v1/transformation'})

@bp.route('/transformation/<uuid:transformation_uuid>', methods=['GET'])
def get_transformation(transformation_uuid):
    # Add logic to get a transformation by UUID
    return jsonify({'message': 'GET /v1/transformation/{transformation_uuid}'})

