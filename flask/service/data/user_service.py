from datetime import datetime
import traceback
from sqlalchemy.orm.exc import NoResultFound

from model.db_base import db
from model.model_import import User, Company
from util.logger import logger


def read_user(data):
    logger.info('Get user list')
    logger.info(f'Filter: {data}')
    condition = {k: v for k, v in data.items() if v is not None}
    query = db.session.query(User).filter_by(**condition).all()
    return query


def create_user(data, current_user=None):
    logger.info("User registration")
    now = datetime.utcnow()
    try:
        query = User.query.filter_by(userid=data.get('userid')).first()
        if query is not None:
            logger.error("Userid already exists")
            return {'message': 'userid already exists'}, 409

        comp_name = data.get('company')
        if comp_name is None:
            return {'message': 'Company name is empty.'}, 400

        data.update({
            'company': Company.query.filter_by(name=comp_name).one(),
            'created': now,
            'created_by': current_user,
            'last_edited': now,
            'edited_by': current_user,
            'is_admin': False,
            'is_deleted': False
        })

        user = User(**data)
        user.hash_password()
        db.session.add(user)
        db.session.commit()

        logger.info('User registration successful')
        return {'message': 'User registration successful'}, 201
    except NoResultFound as e:
        return {'message': 'Company name is empty.'}, 400
    except Exception as e:
        errmsg = 'User registration failed for unknown reason'
        logger.error(errmsg)
        logger.debug(traceback.format_exc())
        raise Exception(errmsg)


def update_user(data):
    pass


def delete_user(data):
    pass