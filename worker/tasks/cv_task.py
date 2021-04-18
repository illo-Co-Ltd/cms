import traceback

from celery.utils.log import get_task_logger
from celery.exceptions import TaskError
import numpy as np

from app import app
from cv import blur, color, detection, normalize, segmentation, threshold

logger = get_task_logger(__name__)


@app.task(name='cv_task.cv_color')
def cv_color(src: np.ndarray, **kwargs) -> np.ndarray:
    try:
        src = cv2
        color.apply(src, )
    except Exception as e:
        logger.error(traceback.format_exc())
        raise TaskError(e)


@app.task(name='cv_task.cv_blur')
def cv_blur(src: np.ndarray, **kwargs) -> np.ndarray:
    return blur.apply(src, **kwargs)


@app.task(name='cv_task.cv_normalize')
def cv_normalize(src: np.ndarray, **kwargs) -> np.ndarray:
    pass


@app.task(name='cv_task.cv_detection')
def cv_detection(src: np.ndarray, **kwargs) -> np.ndarray:
    pass


@app.task(name='cv_task.cv_segmentation')
def cv_segmentation(src: np.ndarray, **kwargs) -> np.ndarray:
    pass


@app.task(name='cv_task.cv_threshold')
def cv_threshold(src: np.ndarray, **kwargs) -> np.ndarray:
    pass
