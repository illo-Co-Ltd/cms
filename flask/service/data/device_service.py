import traceback
from datetime import datetime
from flask_jwt_extended import current_user

from model.db_base import db
from model.model_import import Device, Company, User

from util.logger import logger


def read_device(**kwargs):
    logger.info('Get device list')
    logger.info(f'Filter: {kwargs}')
    try:
        condition = {k: v for k, v in kwargs.items() if v is not None}
        query = db.session.query(Device).filter_by(**condition).all()
        return query
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def create_device(**kwargs):
    logger.info('Register new device')
    now = datetime.utcnow()
    try:
        query = Device.query.filter_by(serial=kwargs.get('serial')).first()
        if query is not None:
            logger.error("Device already exists")
            return {'message': 'Device already exists'}, 409

        company = db.session.query(Company).filter_by(name=kwargs.get('company')).one()
        owner = db.session.query(User).filter_by(userid=kwargs.get('owner')).one()
        device = Device(
            model=kwargs.get('model'),
            serial=kwargs.get('serial'),
            company=company,
            owner=owner,
            ip=kwargs.get('ip'),
            created=now,
            created_by=kwargs.get('created_by', current_user),
            last_edited=now,
            edited_by=kwargs.get('edited_by', current_user),
            is_deleted=False
        )
        db.session.add(device)
        db.session.commit()
        return {'message': f'Posted device<{kwargs.get("serial")}> to db.'}, 201
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def update_device(**kwargs):
    logger.info('Update existing device')
    now = datetime.utcnow()
    try:
        query = db.session.query(Device).filter_by(serial=kwargs.get('serial')).one()
        if kwargs.get('newserial'):
            query.serial = kwargs.get('newserial')
        if kwargs.get('model'):
            query.model = kwargs.get('model')
        if kwargs.get('company'):
            query.company = db.session.query(Company).filter_by(name=kwargs.get('company')).one()
        if kwargs.get('ip'):
            query.ip = kwargs.get('ip')
        if kwargs.get('owner'):
            query.owner = db.session.query(User).filter_by(userid=kwargs.get('owner')).one()
        query.edited = now
        query.edited_by = current_user
        db.session.commit()
        return {'message': f'Updated device<{query.serial}> from db.'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def delete_device(**kwargs):
    logger.info('Delete existing device')
    try:
        query = db.session.query(Device).filter_by(**kwargs).one()
        db.session.delete(query)
        db.session.commit()
        return {'message': f'Deleted device<{query.serial}> from db.'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
