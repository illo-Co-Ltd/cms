from flask_restplus import Namespace, fields

api_status = Namespace('status', description='Status monitoring API')


class FlaskStatusDTO:
    api = api_status
    status = api.model('flask_status', {
        'name': fields.String(required=True, description='Flask status for healthcheck'),
    })


class FlaskConfigDTO:
    api = api_status
    config = api.model('config', {
        'test': fields.String(required=True, description='test'),
    })


class CeleryStatusDTO:
    api = api_status
    status = api.model('celery_status', {
        'alive': fields.Boolean(required=True, description='Connection status'),
    })


class DeviceStatusDTO:
    api = api_status
    status = api.model('device_status', {
        'alive': fields.Boolean(required=True, description='Connection status'),
    })
