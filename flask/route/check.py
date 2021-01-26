from flask import Blueprint, jsonify, current_app

from util.logger import logger

check_route = Blueprint('check_route', __name__)


# sanity check route
@check_route.route('/', methods=['GET'])  # , endpoint='health_check')
def health_check():
    logger.info("This is root url.")
    return jsonify('This is Docker Test developments Server')


@check_route.route('/config', methods=['GET'])
def config_check():
    logger.info("This is root url.")
    return jsonify(str(dict(current_app.config)))
