from flask import Blueprint, jsonify

from tasks.cv_task import add, add_result, capture
from util.logger import logger

camera_route = Blueprint('camera_route', __name__)

@camera_route.route('/add/<a>/<b>/<wait>', methods=['GET'])
def task_add(a, b, wait):
    logger.info("celery tasks test. add.")
    task_id = add(int(a), int(b), int(wait))
    return jsonify(f'task_id:{task_id}')


@camera_route.route('/result/<task_id>', methods=['GET'])
def task_add_result(task_id):
    logger.info("celery result")
    value = add_result(task_id)
    return jsonify(value)


@camera_route.route('/capture', methods=['GET'])
def img_capture():
    logger.info('Capture with camera')
    task_id = capture()
    return jsonify(task_id)
