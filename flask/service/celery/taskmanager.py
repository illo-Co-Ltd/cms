from celery import Celery

from service.celery import celeryconfig

celery_app = Celery('cam_worker')
celery_app.config_from_object(celeryconfig)


class TaskManager:
    def __init__(self):
        pass

    def list_all_tasks(self):
        pass
