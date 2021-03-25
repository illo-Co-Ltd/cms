from model.db_base import db
from model.model_import import Project

from util.logger import logger


def read_project(data):
    logger.info('Get project list')
    logger.info(f'Filter: {data}')
    condition = {k: v for k, v in data.items() if v is not None}
    query = db.session.query(Project).filter_by(**condition).all()
    return query


def create_project(data):
    logger.info('Register new project')
    try:
        project = Project(**data)
        db.session.add(project)
        db.session.commit()
        return {'message': f'Posted project<{data.get("name")}> to db.'}, 201
    except Exception as e:
        logger.error(e)
        raise e
