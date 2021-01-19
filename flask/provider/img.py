from flask import Blueprint, request, jsonify, current_app
from util.logger import logger
from model import user_model
from model import image_model
from util.auth_util import token_required

import jwt
import datetime

image_route = Blueprint('image_route', __name__)


@image_route.route('/list', methods=['GET'])
@token_required
def list_image(current_user):
    logger.info('Get image list')
    image_list = image_model.Image.query.all()
    return jsonify([i.to_dict() for i in image_list])
