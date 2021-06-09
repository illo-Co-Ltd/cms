from flask import current_app
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from router.dto.status_dto import api_status
from service.control_service import add_schedule
from util.logger import logger
from service.celery import camera

api = api_status


# sanity check route
@api.route('/health')
@api.response(200, 'OK')
class Health(Resource):
    @api.doc('Check backend health')
    def get(self):
        logger.info("Health checking")
        return {'msg': 'Server online'}


@api.route('/config')
@api.response(200, 'OK')
class Config(Resource):
    @api.doc('Check flask config')
    def get(self):
        logger.info('Checking config')
        # TODO
        # 권한에 따라 다르게 동작하도록 변경
        if current_app.config['ENV'] == 'development':
            return {k:str(v) for k,v in current_app.config.items()}
        else:
            return None


@api.route('/celery')
@api.response(200, 'OK')
class Celery(Resource):
    @api.doc('Check celery status')
    def get(self):
        logger.info("This is celery check url.")
        return camera.test_connection()


@api.route('/test')
@api.response(200, 'OK')
class Test(Resource):
    @api.doc('test func')
    def get(self):
        add_schedule()
