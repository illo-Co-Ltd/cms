from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace

from util.logger import logger
from tasks import cam_task

api = Namespace('check', description='Status check API')


# sanity check route
@api.route('/health')
@api.response(200, 'OK')
class Health(Resource):
    @api.doc('Check backend health')
    def get(self):
        logger.info("This is root url.")
        return {'msg': 'Server is ok.'}


@api.route('/config')
@api.response(200, 'OK')
class Config(Resource):
    @api.doc('Check flask config')
    def get(self):
        logger.info("This is config check url.")
        return dict(current_app.config)


@api.route('/celery')
@api.response(200, 'OK')
class Celery(Resource):
    @api.doc('Check celery status')
    def get(self):
        logger.info("This is celery check url.")
        task_id = cam_task.add(1, 2, 1)
        return jsonify(task_id)
