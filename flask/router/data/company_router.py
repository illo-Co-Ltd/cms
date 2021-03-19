from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.dto import CompanyDTO
from service.company_service import create_company, read_company

api = CompanyDTO.api
_company = CompanyDTO.company


@api.route('')
class Company(Resource):
    @api.doc('Query company with filters')
    @api.response(200, 'OK')
    @api.response(404, 'No result found for query')
    @api.marshal_list_with(_company, envelope='data')
    @jwt_required()
    def get(self):
        result = read_company({
            'name': request.args.get('name'),
            'subscription': request.args.get('subscription'),
            'expiration_date': request.args.get('expiration_date'),
        })
        return result

    @api.doc('Create new company')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_company, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_company(data)
        except ValueError:
            api.abort(400, message='Wrong date format for expiration_date.')
        except Exception:
            api.abort(500, message='failed to register company')
