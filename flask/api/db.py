import os
import datetime
import json
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from deprecated import deprecated

from models.db_base import db
from models.model import *

from util.logger import logger

crud_route = Blueprint('crud_route', __name__)


@crud_route.route('/company', methods=["GET"])
@jwt_required()
def get_company():
    logger.info("Get company list")
    company_all = Company.query.all()
    result = [x.to_dict() for x in company_all]
    return jsonify({
        'success': True,
        'msg': f'Returned {len(result)} items.',
        'data': result
    }), 200


@crud_route.route('/company', methods=["POST"])
@jwt_required()
def post_company():
    logger.info("Register new company")
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


@crud_route.route('/device', methods=["GET"])
@jwt_required()
def get_device():
    logger.info("Get device list")
    device_all = Device.query.all()
    result = [x.to_dict() for x in device_all]
    return jsonify({
        'success': True,
        'msg': f'Returned {len(result)} items.',
        'data': result
    }), 200


@crud_route.route('/device', methods=["POST"])
@jwt_required()
def post_device():
    logger.info("Register new device")
    try:
        data = request.get_json()
        model = data.get("model")
        serial = data.get("serial")
        owner = data.get("owner")
        # owner = db.session.query(User).filter_by(name=data.get("owner")).one()
        created_by = data.get("created_by")
        edited_by = data.get("edited_by")

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
    except Exception as e:
        logger.error(e)
        return jsonify({
            'success': False,
            'msg': 'Failed to post device.'
        }), 500


@crud_route.route('/device_entry/<proj_name>', methods=["GET"])
@jwt_required()
def get_device_entry(proj_name):
    logger.info("Get DeviceEntry list of specified project")
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


@crud_route.route('/device_entry', methods=["POST"])
@jwt_required()
def post_device_entry():
    pass


@crud_route.route('/project', methods=["GET"])
@jwt_required()
def get_project():
    logger.info("Get project list")
    project_all = Project.query.all()
    result = [x.to_dict() for x in project_all]
    return jsonify({
        'success': True,
        'msg': f'Returned {len(result)} items.',
        'data': result
    }), 200


@crud_route.route('/project', methods=["POST"])
@jwt_required()
def post_project():
    logger.info("Register new project")
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


@crud_route.route('/target', methods=["GET"])
@jwt_required()
def get_target():
    logger.info("Get target list")
    target_all = Target.query.all()
    result = [x.to_dict() for x in target_all]
    return jsonify({
        'success': True,
        'msg': f'Returned {len(result)} items.',
        'data': result
    }), 200


@crud_route.route('/target', methods=["POST"])
@jwt_required()
def post_target():
    logger.info("Register new target")
    try:
        data = request.get_json()
        pid = db.session.query(Project).filter_by(name=data.get("project")).one().id
        target = Target(
            project=pid,
            type=data.get('type'),
            detail=data.get('detail'),
            name=data.get('name'),
            description=data.get('description')
        )
        db.session.add(target)
        db.session.commit()
        return jsonify({
            'success': True,
            'msg': f'Posted target<{data.get("name")}> to db.',
            'data': target.to_dict()
        }), 200
    except NoResultFound as e:
        logger.error(e)
        return jsonify({
            'success': False,
            'msg': f'Cannot find project<{data.get("project")}>.',
        }), 404
    except Exception as e:
        logger.error(e)
        return jsonify({
            'success': False,
            'msg': 'failed to register device'
        }), 500


@crud_route.route('/image', methods=['GET'])
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


@crud_route.route('/image/tree', methods=['GET'])
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
                                'type', 'target',
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
    from target t
             left join image i on t.id = i.target
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


@deprecated
@crud_route.route('/image/test', methods=['GET'])
def create_test():
    from datetime import datetime, timedelta
    comp = db.session.query(Company).first() or Company(
        name='illo.Co.Ltd',
        subscription=True,
        expiration_date=datetime.now() + timedelta(days=7)
    )
    db.session.add(comp)

    user = db.session.query(User).first() or User(
        userid='tester1',
        password='1234',
        username='tester',
        company=comp.id,
        created=datetime.now(),
        last_edited=datetime.now(),
        is_admin=True,
        is_deleted=False
    )
    db.session.add(user)

    prj1 = db.session.query(Project).filter_by(name='Project1').first() or Project(
        name='Project1',
        shorthand='PRJ1',
        description='this is for test',
    )
    prj2 = db.session.query(Project).filter_by(name='Project2').first() or Project(
        name='Project2',
        shorthand='PRJ2',
        description='this is for test',
    )
    db.session.add_all([prj1, prj2])
    targets = db.session.query(Project).all()[:4]
    if len(targets) < 4:
        targets = [
            Target(
                project=prj1.id,
                type='B cell',
                detail='Plasma',
                name='2021B1',
                description='this is for test',
            ),
            Target(
                project=prj1.id,
                type='B cell',
                detail='Plasma',
                name='2021B2',
                description='this is for test',
            ),
            Target(
                project=prj2.id,
                type='T cell',
                detail='Helper',
                name='2021T1',
                description='this is for test',
            ),
            Target(
                project=prj2.id,
                type='T cell',
                detail='Killer',
                name='2021T2',
                description='this is for test',
            )]
        db.session.add_all(targets)
    device = db.session.query(Device).first() or Device(
        model='PROTO1',
        serial='SN654626164',
        company=comp.id,
        owner=user.id,
        ip='0.0.0.0',
        created=datetime.now(),
        created_by=user.id,
        last_edited=datetime.now(),
        edited_by=user.id,
        is_deleted=False
    )
    db.session.add(device)

    image = db.session.query(Image).first()
    mapper = {
        'target': [targets[0].id] * 3 + [targets[1].id] * 2 + [targets[2].id] * 4 + [targets[3].id],
        'path': list(filter(lambda x: x.endswith('.jpg'), os.listdir('/data'))),
        'device': [device.id] * 10,
        'created': [datetime.now()] * 10,
        'created_by': [user.id] * 10,
        'label': ['test image'] * 10,
        'offset_x': [1] * 10,
        'offset_y': [1] * 10,
        'offset_z': [1] * 10,
        'pos_x': [1] * 10,
        'pos_y': [1] * 10,
        'pos_z': [1] * 10,
    }
    logger.info(len(mapper['path']))
    logger.info(mapper['path'])
    if not image:
        db.session.add_all(
            [Image(**{k: l[i] for k, l in mapper.items()}) for i in range(10)]
        )
    db.session.commit()
    return jsonify('10 test records added to database'), 200
