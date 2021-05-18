import os
import traceback
from datetime import datetime

from flask import send_file
from flask_jwt_extended import current_user

from model.db_base import db
from model import Image, Cell, Device

from util.logger import logger

def read_image(path):
    try:
        if os.path.isfile(path):
            return send_file('/data/' + path, mimetype='image/jpg')
        else:
            raise FileNotFoundError
    except Exception as e:
        logger.error(e),
        logger.debug(traceback.format_exc())
        raise e


def create_image(path):
    pass


def delete_image(**kwargs):
    logger.info('Delete image file')
    logger.info(f'Args: {kwargs}')
    try:
        os.remove()
    except Exception as e:
        logger.error(e),
        logger.debug(traceback.format_exc())
        raise e



def read_image_metadata(**kwargs):
    logger.info('Get image list')
    logger.info(f'Filter: {kwargs}')
    try:
        condition = {k: v for k, v in kwargs.items() if v is not None}
        query = db.session.query(Image).filter_by(**condition).all()
        return query
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def create_image_metadata(**kwargs):
    logger.info('create image metadata')
    now = datetime.utcnow()
    try:
        cell = db.session.query(Cell).filter_by(name=kwargs.get('cell')).one()
        device = db.session.query(Device).filter_by(name=kwargs.get('device')).one()
        image = Image(
            path=kwargs.get('path'),
            cell=cell,
            device=device,
            created=now,
            created_by=kwargs.get('created_by', current_user),
            label=kwargs.get('label'),
            offset_x=kwargs.get('offset_x'),
            offset_y=kwargs.get('offset_y'),
            offset_z=kwargs.get('offset_z'),
            pos_x=kwargs.get('pos_x'),
            pos_y=kwargs.get('pos_y'),
            pos_z=kwargs.get('pos_z')
        )
        db.session.add(image)
        db.session.commit()
        return {'message': f'Posted image<{kwargs.get("name")}> to db.'}, 201
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def update_image_metadata(**kwargs):
    logger.info('Update existing image metadata')
    now = datetime.utcnow()
    try:
        query = db.session.query(Image).filter_by(path=kwargs.get('path')).one()

        if kwargs.get('cell'):
            query.cell = kwargs.get('cell')
        if kwargs.get('device'):
            query.device = db.session.query(Device).filter_by(serial=kwargs.get('device')).one()
        if kwargs.get('label'):
            query.label = kwargs.get('label')
        if kwargs.get('offset_x'):
            query.offset_x = kwargs.get('offset_x')
        if kwargs.get('offset_y'):
            query.offset_y = kwargs.get('offset_y')
        if kwargs.get('offset_z'):
            query.offset_z = kwargs.get('offset_z')
        if kwargs.get('pos_x'):
            query.pos_x = kwargs.get('pos_x')
        if kwargs.get('pos_y'):
            query.pos_y = kwargs.get('pos_y')
        if kwargs.get('pos_z'):
            query.pos_z = kwargs.get('pos_z')

        query.edited = now
        query.edited_by = current_user
        db.session.commit()
        return {'message': f'Updated image metadata<{query.serial}> from db.'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def delete_iamge_metadata(**kwargs):
    logger.info('Delete existing image metadata')
    try:
        query = db.session.query(Device).filter_by(**kwargs).one()
        db.session.delete(query)
        db.session.commit()
        return {'message': f'Deleted image metadata<{query.serial}> from db.'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
