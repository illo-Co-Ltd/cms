from flask_restplus import Namespace, fields

api_control = Namespace('control', description='Device control API')


class CaptureDTO:
    api = api_control
    model = api.model('capture', {
        'serial': fields.String(required=True, description='Target device'),
        'project': fields.String(required=True, description='Project name'),
        'cell': fields.String(required=True, description='Cell name'),
        'label': fields.String(required=False, description='Label for extra data'),
        'debug': fields.Boolean(required=False, description='Flag for skipping integrity check'),
    })


class TimelapseDTO:
    api = api_control
    model = api.model('timelapse', {
        'serial': fields.String(required=True, description='Target device'),
        'project': fields.String(required=True, description='Project name'),
        'cell': fields.String(required=True, description='Cell name'),
        'label': fields.String(required=False, description='Label for extra data'),
        'run_every': fields.Float(required=True, description='Timelapse interval.(float seconds)'),
        'expire_at': fields.DateTime(required=True, description='Expiration time'),
        'debug': fields.Boolean(required=False, description='Flag for skipping integrity check'),
    })


class RangeDTO:
    api = api_control
    model = api.model('posrange', {
        'serial': fields.String(required=True, description='Target device'),
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
        'serial': fields.String(required=True, description='Target device'),
        'x': fields.Integer(required=True, description='x position of camera'),
        'y': fields.Integer(required=True, description='y position of camera'),
        'z': fields.Integer(required=False, description='z position of camera'),
    })


class FocusDTO:
    api = api_control
    model = api.model('focus', {
        'serial': fields.String(required=True, description='Target device'),
        'value': fields.Integer(required=True, description='Focus value', min=0, max=255),
    })


class LedDTO:
    api = api_control
    model = api.model('led', {
        'serial': fields.String(required=True, description='Target device'),
        'value': fields.Integer(required=True, description='Focus value', min=0, max=255),
    })
