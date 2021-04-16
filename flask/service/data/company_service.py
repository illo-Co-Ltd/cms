import traceback
from model.db_base import db
from model.model_import import Company

from util.logger import logger


def read_company(data):
    logger.info('Get company list')
    logger.info(f'Filter: {data}')
    condition = {k: v for k, v in data.items() if v is not None}
    query = Company.query.filter_by(**condition).all()
    return query, 200


def create_company(data):
    logger.info('Register new company')
    try:
        query = Company.query.filter_by(name=data.get('name')).first()
        if query is not None:
            logger.error("Company name already exists")
            return {'message': 'name already exists'}, 409

        company = Company(
            name=data.get('name'),
            subscription=data.get('subscription'),
            expiration_date=data.get('expiration_date')
        )
        db.session.add(company)
        db.session.commit()
        return {'message': f'Posted company<{data.get("name")}> to db.'}, 201
    except Exception as e:
        errmsg = 'Company registration failed for unknown reason'
        logger.error(errmsg)
        logger.debug(traceback.format_exc())
        raise Exception(errmsg)
