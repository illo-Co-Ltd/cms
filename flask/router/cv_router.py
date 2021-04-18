from flask import Blueprint, request, jsonify, make_response, send_file
from flask_jwt_extended import jwt_required

from service.cv_service import *

cv_route = Blueprint('cv_route', __name__)


# TODO
# parameter 검사로직 구현

@cv_route.route('/color', methods=['POST'])
@jwt_required()
def r_color():
    data = request.get_json()
    path = data.get('path')
    params = data.get('params')

    return jsonify(s_color(path, params)), 201


@cv_route.route('/blur', methods=['POST'])
@jwt_required()
def r_blur():
    data = request.get_json()
    path = data.get('path')
    params = data.get('params')
    return jsonify(s_blur(path, params)), 201


@cv_route.route('/normalize', methods=['POST'])
@jwt_required()
def r_normalize():
    data = request.get_json()
    path = data.get('path')
    params = data.get('params')
    return jsonify(s_normalize(path, params)), 201


@cv_route.route('/threshold', methods=['POST'])
@jwt_required()
def r_threshold():
    data = request.get_json()
    path = data.get('path')
    params = data.get('params')
    return jsonify(s_threshold(path, params)), 201


@cv_route.route('/result/<task_id>', methods=['GET'])
@jwt_required()
def r_result(task_id):
    return send_file(s_result(task_id).get(), mimetype='image/jpg')
