from flask_restplus import Namespace, fields

api_control = Namespace('control', description='Device control API')


class CaptureDTO:
    api = api_control
    model = api.model('capture', {
        'project': fields.String(required=True, description='Project name'),
        'cell': fields.String(required=True, description='Cell name'),
        'device': fields.String(required=True, description='Device serial'),
        'label': fields.String(required=False, description='Label for extra data'),
        'debug': fields.Boolean(required=False, description='Flag for skipping integrity check'),
    })


class TimelapseDTO:
    api = api_control
    model = api.model('timelapse', {
        'project': fields.String(required=True, description='Project name'),
        'cell': fields.String(required=True, description='Cell name'),
        'device': fields.String(required=True, description='Device serial'),
        'label': fields.String(required=False, description='Label for extra data'),
        'run_every': fields.Float(required=True, description='Timelapse interval.(float seconds)'),
        'expire_at': fields.DateTime(required=True, description='Expiration time'),
        'debug': fields.Boolean(required=False, description='Flag for skipping integrity check'),
    })


class RangeDTO:
    api = api_control
    model = api.model('posrange', {
        'x_min': fields.Integer(required=True, description='x lower limit'),
        'x_max': fields.Integer(required=True, description='x upper limit'),
        'y_min': fields.Integer(required=True, description='y lower limit'),
        'y_max': fields.Integer(required=True, description='y upper limit'),
        'z_min': fields.Integer(required=False, description='z lower limit'),
        'z_max': fields.Integer(required=False, description='z upper limit'),
    })


class PositionDTO:
    api = api_control
    model = api.model('position', {
        'x': fields.Integer(required=True, description='x position of camera'),
        'y': fields.Integer(required=True, description='y position of camera'),
        'z': fields.Integer(required=False, description='z position of camera'),
    })


class FocusDTO:
    api = api_control
    model = api.model('focus', {
        'value': fields.Integer(required=True, description='Focus value', min=0, max=255),
    })


class LedDTO:
    api = api_control
    model = api.model('led', {
        'value': fields.Integer(required=True, description='Focus value', min=0, max=255),
    })
