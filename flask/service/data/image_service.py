import traceback

from flask_jwt_extended import get_jwt_identity

from model.db_base import db
from model.model_import import Image, Cell, Device

from util.logger import logger


def read_image_path(data):
    logger.info('Get image list')
    logger.info(f'Filter: {data}')
    try:
        condition = {k: v for k, v in data.items() if v is not None}
        query = db.session.query(Image).filter_by(**condition).all()
        return query
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def create_image_metadata(data):
    logger.info('Register new image')
    try:
        cell = db.session.query(Cell).filter_by(name=data.get('cell')).one()
        device = db.session.query(Device).filter_by(name=data.get('device')).one()
        image = Image(
            cell=cell,
            path=data.get('path'),
            device=device,
            created=data.get('created'),
            created_by=get_jwt_identity(),
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
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
