import os
import datetime
import json
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from deprecated import deprecated

from model.db_base import db
from model.model_import import *

from util.logger import logger

db_route = Blueprint('crud_route', __name__)


@db_route.route('/company', methods=['GET'])
@jwt_required()
def get_company():
    logger.info('Get company list')
    company_all = Company.query.all()
    result = [x.to_dict() for x in company_all]
    return jsonify({
        'success': True,
        'msg': f'Returned {len(result)} items.',
        'data': result
    }), 200


@db_route.route('/company', methods=['POST'])
@jwt_required()
def post_company():
    logger.info('Register new company')
    try:
        data = request.get_json()
        company = Company(
            name=data.get('name'),
            subscription=data.get('subscription'),
            expiration_date=datetime.strptime(
                data.get('expiration_date'), '%Y-%m-%d'
            )
        )
        db.session.add(company)
        db.session.commit()
        return jsonify({
            'success': True,
            'msg': f'Posted company<{data.get("name")}> to db.',
            'data': company.to_dict()
        }), 200
    except ValueError as e:
        logger.error(e)
        return jsonify({
            'success': False,
            'msg': 'Wrong date format for expiration_date.'
        }), 400
    except Exception as e:
        logger.error(e)
        return jsonify({
            'success': False,
            'msg': 'failed to register device'
        }), 500


@db_route.route('/device', methods=['GET'])
@jwt_required()
def get_device():
    logger.info('Get device list')
    device_all = Device.query.all()
    result = [x.to_dict() for x in device_all]
    return jsonify({
        'success': True,
        'msg': f'Returned {len(result)} items.',
        'data': result
    }), 200


@db_route.route('/device', methods=['POST'])
@jwt_required()
def post_device():
    logger.info('Register new device')
    try:
        data = request.get_json()
        model = data.get('model')
        serial = data.get('serial')
        owner = db.session.query(User).filter_by(name=data.get('owner')).one()
        created_by = current_user.id
        edited_by = current_user.id

        device = Device(
            model=model,
            serial=serial,
            owner=owner,
            created=datetime.datetime.utcnow(),
            created_by=created_by,
            last_edited=datetime.datetime.utcnow(),
            edited_by=edited_by,
            is_deleted=False
        )
        db.session.add(device)
        db.session.commit()
        return jsonify({
            'success': True,
            'msg': f'Posted device<{data.get("serial")}> to db.',
            'data': device.to_dict()
        }), 200
    except NoResultFound as e:
        logger.error(e)
        return jsonify({
            'success': False,
            'msg': f'No user found for owner \"{data.get("owner")}\"'
        }), 404
    except Exception as e:
        logger.error(e)
        return jsonify({
            'success': False,
            'msg': 'Failed to post device.'
        }), 500


@db_route.route('/device_entry/<proj_name>', methods=['GET'])
@jwt_required()
def get_device_entry(proj_name):
    logger.info('Get DeviceEntry list of specified project')
    try:
        pid = db.session.query(Project).filter_by(name=proj_name).one()
    except NoResultFound as e:
        logger.error(e)
        return jsonify({
            'success': False,
            'msg': f'Cannot find project<{proj_name}>.',
        }), 404
    device_entry = db.session.query(DeviceEntry).filter_by(project=pid).all()
    result = [x.to_dict() for x in device_entry]
    return jsonify({
        'success': True,
        'msg': f'Returned {len(result)} items.',
        'data': result
    }), 200


@db_route.route('/device_entry/<proj_name>', methods=['POST'])
@jwt_required()
def post_device_entry():
    pass


@db_route.route('/project', methods=['GET'])
@jwt_required()
def get_project():
    logger.info('Get project list')
    project_all = Project.query.all()
    result = [x.to_dict() for x in project_all]
    return jsonify({
        'success': True,
        'msg': f'Returned {len(result)} items.',
        'data': result
    }), 200


@db_route.route('/project', methods=['POST'])
@jwt_required()
def post_project():
    logger.info('Register new project')
    try:
        data = request.get_json()
        project = Project(
            name=data.get('name'),
            shorthand=data.get('shorthand'),
            description=data.get('description')
        )
        db.session.add(project)
        db.session.commit()
        return jsonify({
            'success': True,
            'msg': f'Posted project<{data.get("name")}> to db.',
            'data': project.to_dict()
        }), 200
    except Exception as e:
        logger.error(e)
        return jsonify({
            'success': False,
            'msg': 'failed to register device'
        }), 500



@db_route.route('/image', methods=['GET'])
@jwt_required()
def get_image():
    logger.info('Get image list')
    image_all = Image.query.all()
    result = [x.to_dict() for x in image_all]
    return jsonify({
        'success': True,
        'msg': f'Returned {len(result)} items.',
        'data': result
    }), 200


@db_route.route('/image/tree', methods=['GET'])
@jwt_required()
def get_tree():
    logger.info('Get hierachical structure of image.')
    if not db.session.query(Project).first():
        return jsonify({
            'success': True,
            'msg': 'There is no project.',
            'data': {}
        }), 200
    with db.engine.connect() as conn:
        res = conn.execute(
            """select json_object(
    'type','project',
    'name', p.name,
    'children', json_arrayagg(json_object(
                                'type', 'cell',
                                'name', t.name,
                                'children', t.children
                                ))
) as json
from project p
         left join (
    select t.name,
           t.project,
           json_arrayagg(json_object(
                   'type', 'image',
                   'id', i.id,
                   'path', i.path
               )) as children
    from cell t
             left join image i on t.id = i.cell
    group by t.id
) t on t.project = p.id
group by p.id;""")
        rows = [dict(row)['json'] for row in res]
        logger.info(type(rows))
        logger.info(type(rows[0]))
        ret = {
            'type': 'company',
            'name': 'illo',
            'children': [json.loads(row) for row in rows]
        }
        return jsonify({
            'success': True,
            'msg': 'Returned structured tree.',
            'data': ret
        }), 200
