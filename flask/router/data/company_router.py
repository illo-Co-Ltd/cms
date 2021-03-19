from flask import request
from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from ..util.dto import CompanyDTO
from service.company_service import *
from util.logger import logger

api = CompanyDTO.api
_company = CompanyDTO.company


@api.route('/')
class Cell(Resource):
    @api.doc('query cell with filters')
    @jwt_required()
    def get(self):
        result = read_company({
            'project': request.args.get('project'),
            'type': request.args.get('type'),
            'detail': request.args.get('detail'),
            'name': request.args.get('name'),
        })
        return ({
            'message': f'Returned {len(result)} items.',
            'data': result
        }), 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            create_cell(data)
            return {'message': f'Posted cell<{data.get("name")}> to db.'}, 200
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find project<{data.get("project")}>.')
        except Exception as e:
            logger.error(e)
            api.abort(500, message='failed to register device')
