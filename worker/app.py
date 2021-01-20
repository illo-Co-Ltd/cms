from celery import Celery
import celeryconfig

celery = Celery('app')
celery.config_from_object(celeryconfig)

if __name__ == '__main__':
    celery.start()