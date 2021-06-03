import traceback

from celery.utils.log import get_task_logger
from celery.exceptions import TaskError

from app import app

logger = get_task_logger(__name__)


@app.task(name='test_task.connection_test')
def connection_test(msg: str):
    try:
        return msg + ', world!'
    except Exception as e:
        logger.error(traceback.format_exc())
        raise TaskError(e)
