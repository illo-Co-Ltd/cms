from flask_restplus import Namespace, fields

api_control = Namespace('control', description='Device control API')


class CaptureDTO:
    api = api_control
    cell = api.model('capture', {
        'project': fields.String(attribute='project.name', required=True, description='Parent project'),
        'type': fields.String(required=True, description='Type of the cell'),
        'detail': fields.String(required=True, description='Specification'),
        'name': fields.String(required=True, description='User defined name'),
        'description': fields.String(required=True, description='Additional info'),
    })
