from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from router.data.data_dto import ProjectDTO
from service.data.project_service import create_project, read_project

api = ProjectDTO.api
_project = ProjectDTO.project


@api.route('/project')
class Project(Resource):
    @api.doc('Query project with filters')
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
            return result
        except Exception:
            api.abort(404)

    @api.doc('Create new project')
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
