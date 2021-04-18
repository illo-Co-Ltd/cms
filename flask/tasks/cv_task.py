import traceback

import numpy as np

from .taskmanager import celery_app
from util import logger


def send_color(path, **kwargs):
    try:
        task = celery_app.send_task('cv_task.cv_color', args=[path], kwargs=kwargs)
        return task.id
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def send_blur(path, **kwargs):
    try:
        task = celery_app.send_task('cv_task.cv_blur', args=[path], kwargs=kwargs)
        return task.id
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def send_normalize(path, **kwargs):
    try:
        task = celery_app.send_task('cv_task.cv_normalize', args=[path], kwargs=kwargs)
        return task.id
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def send_threshold(path, **kwargs):
    try:
        task = celery_app.send_task('cv_task.cv_threshold', args=[path], kwargs=kwargs)
        return task.id
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def receive_result(task_id):
    try:
        res = celery_app.AsyncResult(task_id)
        data = res.get()
        res.forget()
        return res
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e
