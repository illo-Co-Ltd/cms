from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from router.dto.data_dto import CellDTO
from service.data.cell_service import create_cell, read_cell

api = CellDTO.api
_cell = CellDTO.cell


@api.route('/cell')
class Cell(Resource):
    @api.doc('Query cell with filters')
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
            return result
        except Exception as e:
            api.abort(404, reason=e)

    @api.doc('Create new cell')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_cell, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_cell(data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find project<{data.get("project")}>.')
        except Exception:
            api.abort(500, message='Failed to register cell')
