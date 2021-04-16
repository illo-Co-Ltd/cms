from datetime import datetime

from model.db_base import db
from model.model_import import Device, Company, User

from util.logger import logger


def read_device(data):
    logger.info('Get device list')
    logger.info(f'Filter: {data}')
    condition = {k: v for k, v in data.items() if v is not None}
    query = db.session.query(Device).filter_by(**condition).all()
    return query


def create_device(data, current_user=None):
    logger.info('Register new device')
    now = datetime.utcnow()
    try:
        query = Device.query.filter_by(serial=data.get('serial')).first()
        if query is not None:
            logger.error("Device already exists")
            return {'message': 'Device already exists'}, 409

        company = db.session.query(Company).filter_by(name=data.get('company')).one()
        owner = db.session.query(User).filter_by(userid=data.get('owner')).one()
        device = Device(
            model=data.get('model'),
            serial=data.get('serial'),
            company=company,
            owner=owner,
            ip=data.get('ip'),
            created=now,
            created_by=data.get('created_by', current_user),
            last_edited=now,
            edited_by=data.get('created_by', current_user),
            is_deleted=False
        )
        db.session.add(device)
        db.session.commit()
        return {'message': f'Posted device<{data.get("name")}> to db.'}, 201
    except Exception as e:
        logger.error(e)
        raise e
