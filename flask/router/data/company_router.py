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
class Company(Resource):
    @api.doc('query company with filters')
    @jwt_required()
    def get(self):
        result = read_company({
            'name': request.args.get('name'),
            'subscription': request.args.get('subscription'),
            'expiration_date': request.args.get('expiration_date'),
        })
        return ({
            'message': f'Returned {len(result)} items.',
            'data': result
        }), 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            create_company(data)
            return {'message': f'Posted company<{data.get("name")}> to db.'}, 200
        except ValueError:
            api.abort(400, message='Wrong date format for expiration_date.')
        except Exception:
            api.abort(500, message='failed to register company')
