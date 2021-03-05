from flask import Blueprint, jsonify, current_app

from util.logger import logger
from tasks import cam_task

check_route = Blueprint('check_route', __name__)


# sanity check route
@check_route.route('/', methods=['GET'])  # , endpoint='health_check')
def health_check():
    logger.info("This is root url.")
    return jsonify('This is CMS Development Server')


@check_route.route('/config', methods=['GET'])
def config_check():
    logger.info("This is config check url.")
    return jsonify(str(dict(current_app.config)))


@check_route.route('/celery', methods=['GET'])
def celery_check():
    logger.info("This is celery check url.")
    task_id = cam_task.add(1, 2, 1)
    return jsonify(task_id)
