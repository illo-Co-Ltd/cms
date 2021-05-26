import traceback

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
