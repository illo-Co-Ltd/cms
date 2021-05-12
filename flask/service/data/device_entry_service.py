from datetime import datetime
from flask_jwt_extended import get_jwt_identity

from model.db_base import db
from model.model_import import DeviceEntry, Project, Device

from util.logger import logger


def read_device_entry(data):
    logger.info('Get device_entry list')
    logger.info(f'Filter: {data}')
    condition = {k: v for k, v in data.items() if v is not None}
    query = db.session.query(DeviceEntry).filter_by(**condition).all()
    return query


def create_device_entry(data):
    logger.info('Register new device_entry')
    now = datetime.utcnow()
    try:
        device= db.session.query(Device).filter_by(serial=data.get('serial')).one()
        project = db.session.query(Project).filter_by(name=data.get('project')).one()
        device_entry = DeviceEntry(
            device=device,
            project=project,
            created=now,
            created_by=get_jwt_identity(),
        )
        db.session.add(device_entry)
        db.session.commit()
        return {'message': f'Posted {device_entry} to db.'}, 201
    except Exception as e:
        logger.error(e)
        raise e
