from datetime import datetime, timezone

from flask_restplus import Namespace, fields

api_data = Namespace('data', description='DB access API')


class CompanyDTO:
    api = api_data
    model = api.model('company', {
        'name': fields.String(required=True, description='[Key] Name of the company'),
    })


class UserDTO:
    api = api_data
    model = api.model('user', {
        'userid': fields.String(required=True, description='[Key] Unique alphabetical user id'),
        'password': fields.String(required=True, description='User password'),
        'username': fields.String(required=True, description='Name of the user'),
        'company': fields.String(attribute='company.name', required=True,
                                 description='Name of the company user belongs to'),
    })


class ProjectDTO:
    api = api_data
    iso_example = datetime.now(timezone.utc).astimezone().isoformat()
    model = api.model('project', {
        'name': fields.String(required=True, description='[Key] Name of the project'),
        'shorthand': fields.String(required=True, description='Initial of project (Maximum 5 letters)'),
        'description': fields.String(required=True, description='description of the project'),
        'created': fields.DateTime(required=True, description='Created datetime', example=iso_example),
        'started': fields.DateTime(required=True, description='Started datetime', example=iso_example),
        'ended': fields.DateTime(required=True, description='Ended datetime', example=iso_example),
        'created_by': fields.String(attribute='create_by.userid', required=True, description='Userid who created'),
    })
    model_put = api.model('project_put', {
        'name': fields.String(required=True, description='[Key] Name of the project'),
        'shorthand': fields.String(required=False, description='Initial of project (Maximum 5 letters)'),
        'description': fields.String(required=False, description='description of the project'),
        'started': fields.DateTime(required=False, description='Started datetime', example=iso_example),
        'ended': fields.DateTime(required=False, description='Ended datetime', example=iso_example),
        'created_by': fields.String(attribute='create_by.userid', required=False, description='Userid who created'),
    })


class DeviceDTO:
    api = api_data
    model = api.model('device', {
        'serial': fields.String(required=True, description='[Key] Device serial number'),
        'model': fields.String(required=True, description='Device model name'),
        'company': fields.String(attribute='company.name', required=True, description='Company belongs to'),
        'owner': fields.String(attribute='owner.userid', required=True, description='Userid of owner'),
        'ip': fields.String(required=True, description='IP address to access'),
    })
    model_post = api.model('device_post', {
        'serial': fields.String(required=True, description='[Key] Device serial number'),
        'model': fields.String(required=True, description='Device model name'),
        'company': fields.String(attribute='company.name', required=True, description='Company belongs to'),
        'owner': fields.String(attribute='owner.userid', required=True, description='Userid of owner'),
        'ip': fields.String(required=True, description='IP address to access'),
        'cgi_id': fields.String(required=True, description='CGI auth ID'),
        'cgi_pw': fields.String(required=True, description='CGI auth PW'),
    })
    model_put = api.model('device_put', {
        'serial': fields.String(required=True, description='[Key] Device serial number'),
        'model': fields.String(required=False, description='Device model name'),
        'newserial': fields.String(required=False, description='New serial number'),
        'company': fields.String(attribute='company.name', required=False, description='Company belongs to'),
        'owner': fields.String(attribute='owner.userid', required=False, description='Userid of owner'),
        'ip': fields.String(required=False, description='IP address to access'),
        'cgi_id': fields.String(required=False, description='CGI auth ID'),
        'cgi_pw': fields.String(required=False, description='CGI auth PW'),
    })


class DeviceEntryDTO:
    api = api_data
    model = api.model('device_entry', {
        'serial': fields.String(attribute='device.serial', required=True, description='[Key] Device serial number'),
        'model': fields.String(attribute='device.model', required=False, description='Device model name'),
        'company': fields.String(attribute='device.company.name', required=False, description='Name of the company'),
        'owner': fields.String(attribute='device.owner.userid', required=False, description='Userid of owner'),
        'ip': fields.String(attribute='device.ip', required=False, description='IP address to access'),
        'project': fields.String(attribute='project.name', required=True, description='[Key] Parent project'),
    })


class CellDTO:
    api = api_data
    model = api.model('cell', {
        'name': fields.String(required=True, description='[Key] User defined name'),
        'project': fields.String(attribute='project.name', required=True, description='Parent project'),
        'type': fields.String(required=True, description='Type of the cell'),
        'detail': fields.String(required=True, description='Specification'),
        'description': fields.String(required=True, description='Additional info'),
    })


class ImageMetadataDTO:
    api = api_data
    model = api.model('image', {
        'path': fields.String(required=True, description='[Key] Saved path'),
        'cell': fields.String(attribute='cell.name', required=True, description='Target cell'),
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
