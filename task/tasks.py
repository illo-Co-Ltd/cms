import os, time
from dotenv import load_dotenv
from celery import Celery
from util.logger import logger

BROKER = os.environ.get('BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

print('hello!!')

if __name__ == '__main__':
    logger.info('Loaded ENV:' + str(list(os.environ)))

    celery = Celery('tasks', broker=BROKER, backend=CELERY_BACKEND)

@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y