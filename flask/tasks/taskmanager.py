import os
from celery import Celery

BROKER = os.environ.get('BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')


class TaskManager:
    def __init__(self):
        pass

    def list_tasks(self):
        pass
