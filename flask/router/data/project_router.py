import sqlalchemy
from flask import request, abort
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm.exc import NoResultFound

from router.dto.data_dto import ProjectDTO
from service.data.project_service import *

api = ProjectDTO.api
_project = ProjectDTO.model


@api.route('/project')
class Project(Resource):
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_project, envelope='data')
    @jwt_required()
    def get(self):
        try:
            result = read_project(
                name=request.args.get('name'),
                shorthand=request.args.get('shorthand'),
                description=request.args.get('description')
            )
            return result
        except Exception as e:
            api.abort(404, reason=str(type(e)))

    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_project, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_project(**data)
        except IntegrityError as e:
            api.abort(400, message='Duplicate entry', reason=str(type(e)))
        except DataError as e:
            api.abort(400, message='Field is too long', reason=str(type(e)))
        except NoResultFound as e:
            api.abort(400, message='Cannot create project<{data.get("name")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Failed to create project', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(404, 'Not found')
    @api.doc(params={
        'name': 'Project name to query (required)',
        'newname': 'New name (optional)',
        'shorthand': 'New shorthand (optional)',
        'description': 'New Description (optional)'
    })
    @jwt_required()
    def put(self):
        data = request.get_json()
        try:
            return update_project(**data)
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find project<{data.get("name")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Failed to update project', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.doc(params={
        'name': 'Project name to query (one of either required)',
        'shorthand': 'New shorthand (one of either required)',
    })
    @jwt_required()
    def delete(self):
        data = request.get_json()
        try:
            return delete_project(**data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find project<{data.get("name")}>.')
        except Exception:
            api.abort(500, message='Failed to delete project')
