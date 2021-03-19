from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from ..util.dto import ProjectDTO
from service.project_service import *
from util.logger import logger

api = ProjectDTO.api
_project = ProjectDTO.project


@api.route('')
class Project(Resource):
    @api.doc('query project with filters')
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_project, envelope='data')
    @jwt_required()
    def get(self):
        try:
            result = read_project({
                'name': request.args.get('name'),
                'shorthand': request.args.get('shorthand'),
                'description': request.args.get('description'),
            })
            logger.info(result)
            return result
        except Exception:
            api.abort(404)

    @api.doc('query project with filters')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_project, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_project(data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find project<{data.get("project")}>.')
        except Exception:
            api.abort(500, message='Failed to register project')
