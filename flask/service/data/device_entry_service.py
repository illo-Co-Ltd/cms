import traceback
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, current_user

from model.db_base import db
from model import DeviceEntry, Project, Device

from util.logger import logger


def read_device_entry(**kwargs):
    try:
        logger.info('Get device_entry list')
        kwargs = dict(filter(lambda x: x[1], kwargs.items()))
        if kwargs.get('serial'):
            kwargs['device'] = db.session.query(Device).filter_by(serial=kwargs.get('serial')).one()
            kwargs.pop('serial')
        if kwargs.get('project'):
            kwargs['project'] = db.session.query(Project).filter_by(name=kwargs.get('project')).one()
        logger.info(f'Filter: {kwargs}')
        query = db.session.query(DeviceEntry).filter_by(**kwargs).all()
        return query
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def create_device_entry(**kwargs):
    logger.info('Register new device_entry')
    now = datetime.utcnow()
    try:
        device = db.session.query(Device).filter_by(serial=kwargs.get('serial')).one()
        project = db.session.query(Project).filter_by(name=kwargs.get('project')).one()
        device_entry = DeviceEntry(
            device=device,
            project=project,
            created=now,
            created_by=current_user,
        )
        db.session.add(device_entry)
        db.session.commit()
        return {'message': f'Posted {device_entry} to db.'}, 201
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def delete_device_entry(**kwargs):
    logger.info('Delete existing device entry')
    try:
        # Delete all entries in project
        kwargs = dict(filter(lambda x: x[1], kwargs.items()))
        if kwargs.get('serial'):
            kwargs['device'] = db.session.query(Device).filter_by(serial=kwargs.get('serial')).one()
            kwargs.pop('serial')
        if kwargs.get('project'):
            kwargs['project'] = db.session.query(Project).filter_by(name=kwargs.get('project')).one()
        query = db.session.query(DeviceEntry).filter_by(**kwargs)#.all()
        logger.info(query)
        cnt = query.delete()
        db.session.commit()
        return {'message': f'Deleted {cnt} results from db.'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
