from model.db_base import db
from model.model_import import Project, Cell

from util import logger


def read_cell(data):
    logger.info('Get cell list')
    query = db.session.query(Cell).filter_by(**data).all()
    return query


def create_cell(data):
    logger.info('Register new cell')
    try:
        pid = db.session.query(Project).filter_by(name=data.get('project')).one().id
        cell = Cell(
            project=pid,
            type=data.get('type'),
            detail=data.get('detail'),
            name=data.get('name'),
            description=data.get('description')
        )
        db.session.add(cell)
        db.session.commit()
        return {'message': f'Posted cell<{data.get("name")}> to db.'}
    except Exception as e:
        logger.error(e)
        raise e
