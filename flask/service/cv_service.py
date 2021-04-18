import traceback

from PIL import Image
import numpy as np

from tasks import cv_task
from util.logger import logger


def s_color(path, params):
    logger.info('Change colormap of image')
    try:
        task_id = cv_task.send_color(path, **params)
        return task_id
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()


def s_blur(path, params):
    logger.info('Blur image')
    try:
        task_id = cv_task.send_blur(path, **params)
        return task_id
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()


def s_normalize(path, params):
    logger.info('Normalize image')
    try:
        task_id = cv_task.send_normalize(path, **params)
        return task_id
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()


def s_threshold(path, params):
    logger.info('Threshold image')
    try:
        task_id = cv_task.send_threshold(path, **params)
        return task_id
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()


def s_result(task_id):
    logger.info('Get processed result')
    return cv_task.receive_result(task_id)
