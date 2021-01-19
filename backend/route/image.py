from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, request, jsonify, current_app

from model.db_base import db as db
from model.user_model import User
from model.company_model import Company
from model.target_model import Target
from model.device_model import Device
from model.project_model import Project
from model.image_model import Image

from util.logger import logger
from util.auth_util import token_required

import jwt
import datetime

image_route = Blueprint('image_route', __name__)


@image_route.route('/tree', methods=['GET'])
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


@image_route.route('/list', methods=['GET'])
@token_required
def list_image(current_user):
    logger.info('Get image list')
    image_list = Image.query.all()
    return jsonify([i.to_dict() for i in image_list])


@image_route.route('/create', methods=['POST'])
@token_required
def create_image(current_user):
    logger.info('Create image metadata')
    try:
        data = request.get_json()
        project = data.get('project')
        target = data.get('target')
        path = data.get('path')
        device = data.get('device')
        created_by = data.get('created_by')
        label = data.get('label')
        offset_x = data.get('offset_x')
        offset_y = data.get('offset_y')
        offset_z = data.get('offset_z')
        pos_x = data.get('pos_x')
        pos_y = data.get('pos_y')
        pos_z = data.get('pos_z')

        image = Image(
            project=project,
            target=target,
            path=path,
            device=device,
            created=datetime.datetime.utcnow(),
            created_by=created_by,
            label=label,
            offset_x=offset_x,
            offset_y=offset_y,
            offset_z=offset_z,
            pos_x=pos_x,
            pos_y=pos_y,
            pos_z=pos_z
        )
        db.session.add(image)
        db.session.commit()
        return jsonify(image.to_dict()), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Fail to create image metadata'}), 200


@image_route.route('/test', methods=['GET'])
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
        'path': [
            'test_20210119-173800.jpg',
            'test_20210119-173801.jpg',
            'test_20210119-173802.jpg',
            'test_20210119-173803.jpg',
            'test_20210119-173813.jpg',
            'test_20210119-173816.jpg',
            'test_20210119-173817.jpg',
            'test_20210119-173818.jpg',
            'test_20210119-173819.jpg',
            'test_20210119-173820.jpg',
        ],
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
    if not image:
        db.session.add_all(
            [Image(**{k: l[i] for k, l in mapper.items()}) for i in range(10)]
        )
    db.session.commit()
    return jsonify('10 test records added to database'), 200
