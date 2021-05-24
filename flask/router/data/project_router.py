from datetime import datetime

from flask import request
from flask_restplus import Resource, reqparse
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError, StatementError
from sqlalchemy.orm.exc import NoResultFound

from router.dto.data_dto import ProjectDTO
from service.data.project_service import *

api = ProjectDTO.api

parser_get = reqparse.RequestParser()
parser_get.add_argument('name', type=str, location='args')
parser_get.add_argument('shorthand', type=str, location='args')
parser_get.add_argument('created', type=str, location='args')
parser_get.add_argument('started', type=str, location='args')
parser_get.add_argument('ended', type=str, location='args')
parser_get.add_argument('created_by', type=str, location='args')

parser_delete = reqparse.RequestParser()
parser_delete.add_argument('name', type=str, location='args', required=True)


@api.route('/project')
class Project(Resource):
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(ProjectDTO.model, envelope='data')
    @api.expect(parser_get)
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
    @api.expect(ProjectDTO.model_post, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_project(**data)
        except DataError as e:
            api.abort(400, message='Field is too long', reason=str(type(e)))
        except ValueError as e:
            api.abort(400, message='Invalid datetime format(ISO8601)', reason=str(type(e)))
        except IntegrityError as e:
            api.abort(400, message='Viloated DB data model', reason=str(type(e)))
        except StatementError as e:
            api.abort(400, message='Please specify timezone info in ISO8601 format', reason=str(type(e)))
        except NoResultFound as e:
            api.abort(400, message='Cannot create project<{data.get("name")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Failed to create project', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(404, 'Not found')
    @api.expect(ProjectDTO.model_put)
    @jwt_required()
    def put(self):
        data = request.get_json()
        try:
            return update_project(**data)
        except DataError as e:
            api.abort(400, message='Field is too long', reason=str(type(e)))
        except ValueError as e:
            api.abort(400, message='Invalid datetime format(ISO8601)', reason=str(type(e)))
        except IntegrityError as e:
            api.abort(400, message='Viloated DB data model', reason=str(type(e)))
        except StatementError as e:
            api.abort(400, message='Please specify timezone info in ISO8601 format', reason=str(type(e)))
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find project<{data.get("name")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Failed to update project', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(parser_delete)
    @jwt_required()
    def delete(self):
        try:
            data= parser_delete.parse_args()
            return delete_project(**data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find project<{data.get("name")}>.')
        except Exception:
            api.abort(500, message='Failed to delete project')
