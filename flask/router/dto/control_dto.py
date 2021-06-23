from flask_restplus import Namespace, fields

api_control = Namespace('control', description='Device control API')


class CaptureDTO:
    api = api_control
    model = api.model('capture', {
        'serial': fields.String(required=True, description='Target device'),
        'project': fields.String(required=True, description='Project name'),
        'cell': fields.String(required=True, description='Cell name'),
        'path': fields.String(required=True, description='path to save image'),
        'label': fields.String(required=False, description='Label for extra data'),
        'debug': fields.Boolean(required=False, description='Flag for skipping integrity check'),
    })


class RegionalCaptureDTO:
    api = api_control
    model = api.model('regional_capture', {
        'serial': fields.String(required=True, description='Target device'),
        'project': fields.String(required=True, description='Project name'),
        'cell': fields.String(required=True, description='Cell name'),
        'path': fields.String(required=True, description='path to save image'),
        'label': fields.String(required=False, description='Label for extra data'),
        'start_x': fields.Integer(required=True, description='Start x position'),
        'start_y': fields.Integer(required=True, description='Start y position'),
        'end_x': fields.Integer(required=True, description='End x position'),
        'end_y': fields.Integer(required=True, description='End y positionLabel for extra data'),
        'z': fields.Integer(required=True, description='z position'),
        'width': fields.Integer(required=True, description='Position width of capture area'),
        'height': fields.Integer(required=True, description='Position height of capture area'),
        'focus': fields.Integer(required=True, description='Focus value'),
        'debug': fields.Boolean(required=False, description='Flag for skipping integrity check'),
    })

class RegionalScheduleDTO:
    api = api_control
    region_model = api.model('region',{
        'well_no': fields.Integer(required=True, description='Cell number'),
        'start_x': fields.Integer(required=True, description='Start x position'),
        'start_y': fields.Integer(required=True, description='Start y position'),
        'end_x': fields.Integer(required=True, description='End x position'),
        'end_y': fields.Integer(required=True, description='End y positionLabel for extra data'),
        'z': fields.Integer(required=True, description='z position'),
    })
    model = api.model('regional_schedule', {
        'serial': fields.String(required=True, description='Target device'),
        'project': fields.String(required=True, description='Project name'),
        'cell': fields.String(required=True, description='Cell name'),
        'run_every': fields.Float(required=True, description='Timelapse interval.(float seconds)'),
        'expire_at': fields.DateTime(required=True, description='Expiration time'),
        'path': fields.String(required=True, description='path to save image'),
        'width': fields.Integer(required=True, description='Position width of capture area'),
        'height': fields.Integer(required=True, description='Position height of capture area'),
        'focus': fields.Integer(required=True, description='Focus value'),
        'label': fields.String(required=False, description='Label for extra data'),
        'regions':fields.List(fields.Nested(region_model))
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
        'x': fields.Integer(required=False, description='x position of camera'),
        'y': fields.Integer(required=False, description='y position of camera'),
        'z': fields.Integer(required=False, description='z position of camera'),
    })


class FocusDTO:
    api = api_control
    model = api.model('focus', {
        'serial': fields.String(required=True, description='Target device'),
        'focus': fields.Integer(required=True, description='Focus value', min=0, max=255),
    })


class LedDTO:
    api = api_control
    model = api.model('led', {
        'serial': fields.String(required=True, description='Target device'),
        'led': fields.Integer(required=True, description='Led brightness value', min=0, max=255),
    })


class DelayDTO:
    api = api_control
    model = api.model('delay', {
        'serial': fields.String(required=True, description='Target device'),
        'delay': fields.Integer(required=True, description='Movement delay', min=0, max=9999),
    })


class SimpleSerialDTO:
    api = api_control
    model = api.model('serial', {
        'serial': fields.String(required=True, description='Target device'),
    })


class CGIDTO:
    api = api_control
    model = api.model('cgi', {
        'serial': fields.String(required=True, description='Target device'),
        'cgi': fields.String(required=True, description='cgi(after ip)'),
    })
