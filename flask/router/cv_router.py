import traceback

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from util.logger import logger

cv_route = Blueprint('cv_route', __name__, url_prefix='/cv')


@cv_route.route('/color', methods=['POST'])
@jwt_required()
def color():
    logger.info('Capture with camera')
    try:
        data = request.get_json()
        path = data.get('path')
        params = data.get('params')
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        return jsonify({'message': 'Failed to color'}), 200


@cv_route.route('/blur', methods=['POST'])
@jwt_required()
def blur():
    logger.info('Capture with camera')
    try:
        data = request.get_json()
        path = data.get('path')
        params = data.get('params')
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        return jsonify({'message': 'Failed to blur'}), 200


@cv_route.route('/normalize', methods=['POST'])
@jwt_required()
def normalize():
    logger.info('Capture with camera')
    try:
        data = request.get_json()
        path = data.get('path')
        params = data.get('params')
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        return jsonify({'message': 'Failed to normalize'}), 200


@cv_route.route('/threshold', methods=['POST'])
@jwt_required()
def threshold():
    logger.info('Capture with camera')
    try:
        data = request.get_json()
        path = data.get('path')
        params = data.get('params')
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        return jsonify({'message': 'Failed to threshold'}), 200
