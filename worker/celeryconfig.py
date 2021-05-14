import os

# Broker settings.
broker_url = os.environ.get('BROKER')
# Using the database to store task state and results.
result_backend = os.environ.get('CELERY_BACKEND')
# List of modules to import when the Celery worker starts.
imports = ('worker.cam_task', 'worker.cv_task')
# task specific configuration
task_annotations = {
    'cam_task': {'rate_limit': '10/s'},
    'cv_task': {'rate_limit': '10/s'}
}
# redbeat config
redbeat_redis_url = os.environ.get('REDBEAT_BACKEND')
redbeat_lock_key = None
