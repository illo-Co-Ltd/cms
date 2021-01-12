from flask import Blueprint, jsonify

from util.logger import logger

check_route = Blueprint('check_route', __name__)


# sanity check route
@check_route.route('/', methods=['GET'])
def test_router():
    logger.info("hello this is root url!")
    return jsonify('This is Docker Test developments Server!')
