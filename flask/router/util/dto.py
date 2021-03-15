from flask_restplus import Namespace, fields


class CompanyDTO:
    api = Namespace('company', description='Company operations')
    company = api.model('company', {
        'name': fields.String(required=True, description='Name of the company'),
    })


class UserDTO:
    api = Namespace('user', description='User operations')
    user = api.model('user', {
        'userid': fields.String(required=True, description='Unique alphabetical user id'),
        'password': fields.String(required=True, description='User password'),
        'username': fields.String(required=True, description='Name of the user'),
        'company': fields.String(attribute='company.name', required=True, description='Name of the company user belongs to'),
    })


class ProjectDTO:
    api = Namespace('project', description='Project operations')
    project = api.model('project', {
        'name': fields.String(required=True, description='Name of the project'),
        'shorthand': fields.String(required=True, description='Initial of project (Maximum 5 letters)'),
        'description': fields.String(required=True, description='description of the project'),
    })


class DeviceDTO:
    api = Namespace('device', description='Device operations')
    device = api.model('device', {
        'model': fields.String(required=True, description='Device model name'),
        'serial': fields.String(required=True, description='Device serial number'),
        'company': fields.String(required=True, description='Company belongs to'),
        'owner': fields.String(required=True, description='Administrator of device'),
        'ip': fields.String(required=True, description='IP address to access'),
    })


class DeviceEntryDTO:
    api = Namespace('device_entry', description='DeviceEntry operations')
    device_entry = api.model('device_entry', {
        'device': fields.String(required=True, description='Device serial number'),
        'project': fields.String(required=True, description='Parent project'),
    })


class CellDTO:
    api = Namespace('cell', description='Cell operations')
    cell = api.model('cell', {
        'project': fields.String(required=True, description='Parent project'),
        'type': fields.String(required=True, description='Type of the cell'),
        'detail': fields.String(required=True, description='Specification'),
        'name': fields.String(required=True, description='User defined name'),
        'description': fields.String(required=True, description='Additional info'),
    })


class ImageDTO:
    api = Namespace('image', description='Image operations')
    image = api.model('image', {
        'model': fields.String(required=True, description='Device model name'),
        'serial': fields.String(required=True, description='Device serial number'),
        'company': fields.String(required=True, description='Company belongs to'),
        'owner': fields.String(required=True, description='Administrator of device'),
        'ip': fields.String(required=True, description='IP address to access'),
    })
