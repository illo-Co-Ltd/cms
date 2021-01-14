from flask import Blueprint, jsonify

from util.logger import logger
from task.tasks import add

check_route = Blueprint('check_route', __name__)


# sanity check route
@check_route.route('/', methods=['GET'])  # , endpoint='health_check')
def health_check():
    logger.info("This is root url.")
    return jsonify('This is Docker Test developments Server')


@check_route.route('/add/<a>/<b>/<wait>', methods=['GET'])  # , endpoint='task_add')
def task_add(a, b, wait):
    logger.info("celery task test. add.")
    task = add.apply_async([int(a), int(b), int(wait)])
    return jsonify(f'task_id:{task.id}')


@check_route.route('/result/<task_id>', methods=['GET'])  # , endpoint='task_add_result')
def task_add_result(task_id):
    logger.info("celery result")
    task = add.AsyncResult(task_id)
    value = [value for result, value in task.collect()]
    return jsonify(value)
