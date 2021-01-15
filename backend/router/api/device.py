from flask import Blueprint, request, jsonify, current_app
from util.logger import logger
from model import user_model
from model import device_model
from util.auth_util import token_required

import jwt
import datetime

device_route = Blueprint('device_route', __name__)


@device_route.route('/device', methods=["GET"])
@token_required
def list_device(current_user):
    logger.info("Get device list")
    device_list = device_model.Device.query.all()
    return jsonify([d.to_dict() for d in device_list])


@device_route.route('/device', methods=["POST"])
@token_required
def register_device(current_user):
    logger.info("Register new device")
    try:
        data = request.get_json()
        model = data.get("model")
        serial = data.get("serial")
        owner = data.get("owner")
        created_by = data.get("created_by")
        edited_by = data.get("edited_by")

        db = device_model.db
        device = device_model.Device(
            model=model,
            serial=serial,
            owner=owner,
            created=datetime.datetime.utcnow(),
            created_by=created_by,
            last_edited=datetime.datetime.utcnow(),
            edited_by=edited_by,
            is_deleted=False
        )
        db.session.add(device)
        db.session.commit()
        return jsonify(device.to_dict()), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'failed to register device'}), 200
