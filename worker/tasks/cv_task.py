import os
import traceback

from PIL import Image
from celery.utils.log import get_task_logger
from celery.exceptions import TaskError
import numpy as np
import cv2

from app import app
from cv import blur, color, detection, normalize, segmentation, threshold, equalize_background

logger = get_task_logger(__name__)


# TODO
# task chaining 구현
# image caching 방법 고안


@app.task(name='cv_task.cv_color')
def cv_color(path, **kwargs) -> np.ndarray:
    try:
        src = np.array(Image.open('/data/' + path))
        output_path = '/data/cv/'+path
        if not os.path.exists('/data/cv'):
            os.mkdir('/data/cv')
        Image.fromarray(color.apply(src, **kwargs)).save(output_path)
        return output_path
    except Exception as e:
        logger.error(traceback.format_exc())
        raise TaskError(e)


@app.task(name='cv_task.cv_blur')
def cv_blur(path, **kwargs) -> np.ndarray:
    try:
        src = np.array(Image.open('/data/' + path))
        output_path = '/data/cv/'+path
        if not os.path.exists('/data/cv'):
            os.mkdir('/data/cv')
        Image.fromarray(blur.apply(src, **kwargs)).save(output_path)
        return output_path
    except Exception as e:
        logger.error(traceback.format_exc())
        raise TaskError(e)


@app.task(name='cv_task.cv_normalize')
def cv_normalize(path, **kwargs) -> np.ndarray:
    try:
        src = np.array(Image.open('/data/' + path))
        output_path = '/data/cv/'+path
        if not os.path.exists('/data/cv'):
            os.mkdir('/data/cv')
        Image.fromarray(normalize.apply(src, **kwargs)).save(output_path)
        return output_path
    except Exception as e:
        logger.error(traceback.format_exc())
        raise TaskError(e)


@app.task(name='cv_task.cv_threshold')
def cv_threshold(path, **kwargs) -> np.ndarray:
    try:
        src = np.array(Image.open('/data/' + path))
        output_path = '/data/cv/'+path
        if not os.path.exists('/data/cv'):
            os.mkdir('/data/cv')
        Image.fromarray(threshold.apply(src, **kwargs)).save(output_path)
        return output_path
    except Exception as e:
        logger.error(traceback.format_exc())
        raise TaskError(e)


@app.task(name='cv_task.cv_detection')
def cv_detection(src: np.ndarray, **kwargs) -> np.ndarray:
    pass


@app.task(name='cv_task.cv_segmentation')
def cv_segmentation(src: np.ndarray, **kwargs) -> np.ndarray:
    pass

@app.task(name='cv_task.equalize_background')
def equalize_background(path, **kwargs) -> np.ndarray:
    try:
        src = cv2.imread('/data/' + path)
        output_path = '/data/cv/'+path
        if not os.path.exists('/data/cv'):
            os.mkdir('/data/cv')
        cv2.imwrite(output_path, equalize_background.apply(src, **kwargs))
        return output_path
    except Exception as e:
        logger.error(traceback.format_exc())
        raise TaskError(e)