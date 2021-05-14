import traceback

from model.db_base import db
from model.model_import import Project, Cell

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


def create_cell(data):
    logger.info('Register new cell')
    try:
        pid = db.session.query(Project).filter_by(name=data.get('project')).one().id
        cell = Cell(
            project_id=pid,
            type=data.get('type'),
            detail=data.get('detail'),
            name=data.get('name'),
            description=data.get('description')
        )
        db.session.add(cell)
        db.session.commit()
        return {'message': f'Posted cell<{data.get("name")}> to db.'}, 201
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
