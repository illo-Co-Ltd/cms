from flask import Blueprint, request, jsonify, current_app
from util.logger import logger
from model import user_model
from model import image_model
from util.auth_util import token_required

import jwt
import datetime

image_route = Blueprint('image_route', __name__)


@image_route.route('/image', methods=["GET"])
@token_required
def list_image(current_user):
    logger.info("Get image list")
    image_list = image_model.Image.query.all()
    return jsonify([i.to_dict() for i in image_list])


@image_route.route('/image', methods=["POST"])
@token_required
def create_image(current_user):
    logger.info("Create image metadata")
    try:
        data = request.get_json()
        project = data.get('project')
        target = data.get('target')
        path = data.get('path')
        device = data.get('device')
        created_by = data.get('created_by')
        label = data.get('label')
        offset_x = data.get('offset_x')
        offset_y = data.get('offset_y')
        offset_z = data.get('offset_z')
        pos_x = data.get('pos_x')
        pos_y = data.get('pos_y')
        pos_z = data.get('pos_z')

        db = image_model.db
        image = image_model.Image(
            project=project,
            target=target,
            path=path,
            device=device,
            created=datetime.datetime.utcnow(),
            created_by=created_by,
            label=label,
            offset_x=offset_x,
            offset_y=offset_y,
            offset_z=offset_z,
            pos_x=pos_x,
            pos_y=pos_y,
            pos_z=pos_z
        )
        db.session.add(image)
        db.session.commit()
        return jsonify(image.to_dict()), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Fail to create image metadata'}), 200