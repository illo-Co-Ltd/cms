import traceback
from datetime import datetime

from model import User, Project
from model.db_base import db

from util.logger import logger


def read_project(**kwargs):
    try:
        logger.info('Get project list')
        logger.info(f'Filter: {kwargs}')
        condition = {k: v for k, v in kwargs.items() if v is not None}
        query = db.session.query(Project).filter_by(**condition).all()
        return query
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def create_project(**kwargs):
    logger.info('Register new project')
    try:
        kwargs.update({
            'created':datetime.fromisoformat(kwargs.get('created')),
            'started': datetime.fromisoformat(kwargs.get('started')),
            'ended': datetime.fromisoformat(kwargs.get('ended')),
            'created_by':db.session.query(User).filter_by(userid=kwargs.get('created_by')).one()
        })

        project = Project(**kwargs)
        db.session.add(project)
        db.session.commit()
        return {'message': f'Posted project<{kwargs.get("name")}> to db.'}, 201
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def update_project(**kwargs):
    logger.info('Update existing project')
    try:
        query = db.session.query(Project).filter_by(name=kwargs.get('name')).one()
        if kwargs.get('newname'):
            query.name = kwargs.get('newname')
        if kwargs.get('shorthand'):
            query.shorthand = kwargs.get('shorthand')
        if kwargs.get('description'):
            query.description = kwargs.get('description')
        db.session.commit()
        return {'message': f'Updated project<{query.name}> from db.'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def delete_project(**kwargs):
    logger.info('Delete existing project')
    kwargs = dict(filter(lambda x: x[1], kwargs.items()))
    try:
        query = db.session.query(Project).filter_by(**kwargs).one()
        db.session.delete(query)
        db.session.commit()
        return {'message': f'Deleted project<{query.name}> from db.'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
