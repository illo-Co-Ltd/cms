from model.db_base import db
from model.model_import import Company

from util.logger import logger


def read_company(data):
    logger.info('Get company list')
    logger.info(f'Filter: {data}')
    condition = {k: v for k, v in data.items() if v is not None}
    query = db.session.query(Company).filter_by(**condition).all()
    return query


def create_company(data):
    logger.info('Register new company')
    try:
        company = Company(
            name=data.get('name'),
            subscription=data.get('subscription'),
            expiration_date=data.get('expiration_date')
        )
        db.session.add(company)
        db.session.commit()
        return {'message': f'Posted company<{data.get("name")}> to db.'}
    except Exception as e:
        logger.error(e)
        raise e
