from datetime import datetime
from flask_jwt_extended import current_user

from model.db_base import db
from model.model_import import Device, Company, User

from util.logger import logger


def read_device(data):
    logger.info('Get device list')
    logger.info(f'Filter: {data}')
    condition = {k: v for k, v in data.items() if v is not None}
    query = db.session.query(Device).filter_by(**condition).all()
    return query


def create_device(data):
    logger.info('Register new device')
    now = datetime.utcnow()
    try:
        company = db.session.query(Company).filter_by(username=data.get('company')).one()
        owner = db.session.query(User).filter_by(username=data.get('owner')).one()
        device = Device(
            model=data.get('model'),
            serial=data.get('serial'),
            company=company,
            owner=owner,
            ip=data.get('ip'),
            created=now,
            created_by=current_user,
            last_edited=now,
            edited_by=current_user,
            is_deleted=False
        )
        db.session.add(device)
        db.session.commit()
        return {'message': f'Posted device<{data.get("name")}> to db.'}, 201
    except Exception as e:
        logger.error(e)
        raise e
