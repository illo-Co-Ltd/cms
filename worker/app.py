from celery import Celery
import celeryconfig

app = Celery('worker')
app.config_from_object(celeryconfig)

if __name__ == '__main__':
    app.start()