from flask_restplus import Resource, reqparse
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import HTTPException

from service.explorer_service import *

from router.dto.explorer_dto import *

api = api_explorer
parser_path = reqparse.RequestParser()
parser_path.add_argument('path', type=str, location='args', required=True)


@api.route('/listdir')
class ListDir(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(404, 'Not Found')
    @api.expect(parser_path)
    @api.marshal_with(ListDirDTO.model)
    @jwt_required()
    def get(self):
        try:
            ret = {'children':listdir(parser_path.parse_args().get('path'))}
            logger.info(ret)
            return ret
        except FileNotFoundError as e:
            api.abort(404, message=f'Cannot find directory.', reason=str(type(e)))
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))
