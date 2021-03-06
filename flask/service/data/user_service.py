from datetime import datetime
import traceback
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import get_jwt_identity, current_user

from model.db_base import db
from model.model_import import User, Company
from util.exc import NotEnoughPermission
from util.logger import logger


def read_user(**kwargs):
    try:
        logger.info('Get user list')
        logger.info(f'Filter: {kwargs}')
        condition = {k: v for k, v in kwargs.items() if v is not None}
        query = db.session.query(User).filter_by(**condition).all()
        return query
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def create_user(**kwargs):
    logger.info("User registration")
    now = datetime.utcnow()
    try:
        query = User.query.filter_by(userid=kwargs.get('userid')).first()
        if query is not None:
            logger.error("Userid already exists")
            return {'message': 'userid already exists'}, 409

        comp_name = kwargs.get('company')
        if comp_name is None:
            return {'message': 'Company name is empty.'}, 400

        kwargs.update({
            'company': Company.query.filter_by(name=comp_name).one(),
            'created': now,
            'last_edited': now,
            'is_deleted': False
        })

        user = User(**kwargs)
        user.hash_password()
        db.session.add(user)
        db.session.commit()

        logger.info('User registration successful')
        return {'message': 'User registration successful'}, 201
    except NoResultFound as e:
        return {'message': 'Company doesn\'t exist.'}, 400
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def update_user(**kwargs):
    logger.info('Update existing user')
    now = datetime.utcnow()
    try:
        query = db.session.query(User).filter_by(userid=kwargs.get('userid')).one()
        if kwargs.get('password'):
            query.password = kwargs.get('password')
            query.hash_password()
        if kwargs.get('username'):
            query.username = kwargs.get('username')
        if kwargs.get('company'):
            query.company = db.session.query(Company).filter_by(name=kwargs.get('company')).one()
        if kwargs.get('is_admin'):
            query.is_admin = kwargs.get('is_admin')
        query.edited = now
        query.edited_by = current_user
        db.session.commit()
        return {'message': f'Updated user<{query.userid}> from db.'}, 200
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def delete_user(**kwargs):
    logger.info('Delete existing user')
    try:
        if current_user.is_admin:
            query = db.session.query(User).filter_by(**kwargs).one()
            db.session.delete(query)
            db.session.commit()
            return {'message': f'Deleted user<{query.userid}> from db.'}, 200
        else:
            # TODO
            # Permission 구현
            raise NotEnoughPermission(required=None, obtained=None)

    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
