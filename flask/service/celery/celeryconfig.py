import os

# Broker settings.
broker_url = os.environ.get('BROKER')
# Using the database to store task state and results.
result_backend = os.environ.get('CELERY_BACKEND')
# host for database for metadata
mysql_uri= os.environ.get('MYSQL_URI')
# List of modules to import when the Celery worker starts.
imports = ('tasks.cam_task', 'tasks.cv_task', 'tasks.test_task')
# task specific configuration
task_annotations = {
    'cam_task': {'rate_limit': '10/s'},
    'cv_task': {'rate_limit': '10/s'}
}
# redbeat config
redbeat_redis_url = os.environ.get('REDBEAT_BACKEND')
#redbeat_lock_key = None
beat_max_loop_interval=1
redbeat_lock_timeout=5
