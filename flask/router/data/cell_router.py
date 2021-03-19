from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from ..util.dto import CellDTO
from service.cell_service import *
from util.logger import logger

api = CellDTO.api
_cell = CellDTO.cell


@api.route('')
class Cell(Resource):
    @api.doc('query cell with filters')
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_cell, envelope='data')
    @jwt_required()
    def get(self):
        try:
            result = read_cell({
                'project': request.args.get('project'),
                'type': request.args.get('type'),
                'detail': request.args.get('detail'),
                'name': request.args.get('name'),
            })
            logger.info(result)
            return result
        except Exception:
            api.abort(404)

    @api.doc('query cell with filters')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_cell, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_cell(data), 201
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find project<{data.get("project")}>.')
        except Exception as e:
            logger.error(e)
            api.abort(500, message='Failed to register device')
