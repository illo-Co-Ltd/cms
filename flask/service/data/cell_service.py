import traceback
from datetime import datetime

from flask_jwt_extended import current_user

from model.db_base import db
from model import Project, Cell

from util.logger import logger


def read_cell(data):
    logger.info('Get cell list')
    logger.info(f'Filter: {data}')
    try:
        condition = {k: v for k, v in data.items() if v is not None}
        query = db.session.query(Cell).filter_by(**condition).all()
        return query
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def create_cell(**kwargs):
    logger.info('Register new cell')
    try:
        query = Cell.query.filter_by(name=kwargs.get('name')).first()
        if query is not None:
            logger.error("Cell already exists")
            return {'message': 'Cell already exists'}, 409

        pid = db.session.query(Project).filter_by(name=kwargs.get('project')).one().id
        cell = Cell(
            project_id=pid,
            type=kwargs.get('type'),
            detail=kwargs.get('detail'),
            name=kwargs.get('name'),
            description=kwargs.get('description')
        )
        db.session.add(cell)
        db.session.commit()
        return {'message': f'Posted cell<{kwargs.get("name")}> to db.'}, 201
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def update_cell(**kwargs):
    logger.info('Update existing cell')
    now = datetime.utcnow()
    try:
        query = db.session.query(Cell).filter_by(name=kwargs.get('name')).one()
        if 'newserial' in kwargs.keys():
            query.serial = kwargs.get('newserial')
        if 'model' in kwargs.keys():
            query.model_post = kwargs.get('model')
        if 'company' in kwargs.keys():
            query.company = db.session.query(Company).filter_by(name=kwargs.get('company')).one()
        if 'ip' in kwargs.keys():
            query.ip = kwargs.get('ip')
        if 'owner' in kwargs.keys():
            query.owner = db.session.query(User).filter_by(userid=kwargs.get('owner')).one()
        query.edited = now
        query.edited_by = current_user
        db.session.commit()
        return {'message': f'Updated cell<{query.serial}> from db.'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def delete_cell(**kwargs):
    logger.info('Delete existing cell')
    try:
        query = db.session.query(Device).filter_by(**kwargs).one()
        db.session.delete(query)
        db.session.commit()
        return {'message': f'Deleted cell<{query.serial}> from db.'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
