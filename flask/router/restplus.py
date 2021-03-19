import logging

from flask_restplus import Api, Namespace
from sqlalchemy.orm.exc import NoResultFound
from .. import __version__
log = logging.getLogger(__name__)

api: Api = Api(
    version=__version__,
    title='My API',
    default='???',
    default_label='',
    description='My Rest Api')


def format_uri(entity_name: str) -> str:
    """ Format url from entity name.
    """
    return entity_name.replace('_', '/')


def explode_entity_name(entity_name: str) -> str:
    """ replaces _ with space
    """
    return entity_name.replace('_', ' ')


def name_space(entity_name) -> Namespace:
    """ Get formatted namespace
    """
    return api.namespace(
        format_uri(entity_name),
        description='Operations related to {}'
        .format(explode_entity_name(entity_name)))


@api.errorhandler
def default_error_handler(e):
    """ By default all errors will be handled here
    """
    message = 'An Unhandled exception has occurred'
    log.exception(e)
    return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    """ Database not found
    """
    return {'message': 'A database result was not found'}, 404