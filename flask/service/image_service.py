from flask_jwt_extended import current_user

from model.db_base import db
from model.model_import import Image, Cell, Device

from util.logger import logger


def read_image(data):
    logger.info('Get image list')
    logger.info(f'Filter: {data}')
    condition = {k: v for k, v in data.items() if v is not None}
    query = db.session.query(Image).filter_by(**condition).all()
    return query


def create_image(data):
    logger.info('Register new image')
    try:
        cell = db.session.query(Cell).filter_by(name=data.get('cell')).one()
        device = db.session.query(Device).filter_by(name=data.get('device')).one()
        image = Image(
            cell=cell,
            path=data.get('path'),
            device=device,
            created=data.get('created'),
            created_by=current_user,
            label=data.get('label'),
            offset_x=data.get('offset_x'),
            offset_y=data.get('offset_y'),
            offset_z=data.get('offset_z'),
            pos_x=data.get('pos_x'),
            pos_y=data.get('pos_y'),
            pos_z=data.get('pos_z')
        )
        db.session.add(image)
        db.session.commit()
        return {'message': f'Posted image<{data.get("name")}> to db.'}, 201
    except Exception as e:
        logger.error(e)
        raise e
