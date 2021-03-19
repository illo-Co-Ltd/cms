from flask import Blueprint, request, jsonify, current_app

from model.db_base import db
from model.image_model import Image

from .taskmanager import celery_app
from util.logger import logger

task_callback_route = Blueprint('task_callback_route', __name__)


@task_callback_route.route('/on_capture_success/<task_id>', methods=['GET'])
def on_capture_success(task_id):
    logger.info("Callback triggered: Adding image record of capture.")
    try:
        res = celery_app.AsyncResult(task_id)
        data = res.get()
        res.forget()
        logger.info(f'data: {data}')
        image = Image(
            cell=data.get('cell'),
            path=data.get('path'),
            device=data.get('device'),
            created=data.get('created'),
            created_by=data.get('created_by'),
            label=data.get('label'),
            offset_x=data.get('offset_x'),
            offset_y=data.get('offset_y'),
            offset_z=data.get('offset_z'),
            pos_x=data.get('pos_x'),
            pos_y=data.get('pos_y'),
            pos_z=data.get('pos_z')
        )
        db.session.add(image)
        db.session.commit()
        return jsonify('Successfully registered image record'), 200
    except Exception as e:
        logger.error(e)
        return jsonify('Failed to register image record'), 200


@task_callback_route.route('/on_capture_failure', methods=['GET'])
def on_capture_failure():
    logger.warning('Task failed')