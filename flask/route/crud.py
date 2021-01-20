import os
from flask import Blueprint, request, jsonify, current_app

from model.db_base import db
from model.company_model import Company
from model.user_model import User
from model.device_model import Device
from model.project_model import Project
from model.target_model import Target
from model.image_model import Image

from util.logger import logger
from util.auth_util import token_required

import jwt
import datetime

crud_route = Blueprint('crud_route', __name__)


@crud_route.route('/company', methods=["GET"])
@token_required
def list_company(current_user):
    logger.info("Get company list")
    company_list = Company.query.all()
    return jsonify([x.to_dict() for x in company_list])


@crud_route.route('/company', methods=["POST"])
@token_required
def register_company(current_user):
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
        return jsonify(company.to_dict()), 200
    except ValueError as e:
        logger.error(e)
        return jsonify({'message': 'Wrong date format for expiration_date.'}), 400
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'failed to register device'}), 200


@crud_route.route('/device', methods=["GET"])
@token_required
def list_device(current_user):
    logger.info("Get device list")
    device_list = Device.query.all()
    return jsonify([x.to_dict() for x in device_list])


@crud_route.route('/device', methods=["POST"])
@token_required
def register_device(current_user):
    logger.info("Register new device")
    try:
        data = request.get_json()
        model = data.get("model")
        serial = data.get("serial")
        owner = data.get("owner")
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
        return jsonify(device.to_dict()), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'failed to register device'}), 200


@crud_route.route('/project', methods=["GET"])
@token_required
def list_project(current_user):
    logger.info("Get project list")
    project_list = Project.query.all()
    return jsonify([x.to_dict() for x in project_list])


@crud_route.route('/project', methods=["POST"])
@token_required
def register_project(current_user):
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
        return jsonify(project.to_dict()), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'failed to register device'}), 200


@crud_route.route('/target', methods=["GET"])
@token_required
def list_target(current_user):
    logger.info("Get target list")
    target_list = Target.query.all()
    return jsonify([x.to_dict() for x in target_list])


@crud_route.route('/target', methods=["POST"])
@token_required
def register_target(current_user):
    logger.info("Register new target")
    try:
        data = request.get_json()
        target = Target(
            project=data.get('project'),
            type=data.get('type'),
            detail=data.get('detail'),
            name=data.get('name'),
            description=data.get('description')
        )
        db.session.add(target)
        db.session.commit()
        return jsonify(target.to_dict()), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'failed to register device'}), 200


@crud_route.route('/image', methods=['GET'])
@token_required
def list_image(current_user):
    logger.info('Get image list')
    image_list = Image.query.all()
    return jsonify([x.to_dict() for x in image_list])


@crud_route.route('/image/tree', methods=['GET'])
def get_structure():
    logger.info('Get hierachical structure of image.')
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
        import json
        rows = [dict(row)['json'] for row in res]
        logger.info(type(rows))
        logger.info(type(rows[0]))
        ret = {
            'type': 'company',
            'name': 'illo',
            'children': [json.loads(row) for row in rows]
        }
        return jsonify(ret)


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
