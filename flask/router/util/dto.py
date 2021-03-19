from flask_restplus import Namespace, fields


class CompanyDTO:
    api = Namespace('company', description='Company operations')
    company = api.model('company', {
        'name': fields.String(required=True, description='Name of the company'),
    })


class UserDTO:
    api = Namespace('user', description='User, Authentication operations')
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
        'company': fields.String(attribute='company.name', required=True, description='Company belongs to'),
        'owner': fields.String(attribute='owner.userid', required=True, description='Userid of owner'),
        'ip': fields.String(required=True, description='IP address to access'),
    })


class DeviceEntryDTO:
    api = Namespace('device_entry', description='DeviceEntry operations')
    device_entry = api.model('device_entry', {
        'serial': fields.String(required=True, description='Device serial number'),
        'project': fields.String(required=True, description='Parent project'),
    })


class CellDTO:
    api = Namespace('cell', description='Cell operations')
    cell = api.model('cell', {
        'project': fields.String(attribute='project.name', required=True, description='Parent project'),
        'type': fields.String(required=True, description='Type of the cell'),
        'detail': fields.String(required=True, description='Specification'),
        'name': fields.String(required=True, description='User defined name'),
        'description': fields.String(required=True, description='Additional info'),
    })


class ImageDTO:
    api = Namespace('image', description='Image operations')
    image = api.model('image', {
        'cell': fields.String(attribute='cell.name', required=True, description='Target cell'),
        'path': fields.String(required=True, description='Saved path'),
        'device': fields.String(attribute='device.serial', required=True, description='Used device'),
        'created': fields.DateTime(required=True, description='Created datetime'),
        'created_by': fields.String(attribute='create_by.userid', required=True, description='Userid who created'),
        'label': fields.String(required=True, description='Image label'),
        'offset_x': fields.Integer(required=True, description='Calibrated x offset'),
        'offset_y': fields.Integer(required=True, description='Calibrated y offset'),
        'offset_z': fields.Integer(required=True, description='Calibrated z offset'),
        'pos_x': fields.Integer(required=True, description='x coordinate of point'),
        'pos_y': fields.Integer(required=True, description='y coordinate of point'),
        'pos_z': fields.Integer(required=True, description='z coordinate of point'),
    })
