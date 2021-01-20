import os
# Broker settings.
broker_url = os.environ.get('BROKER')

# List of modules to import when the Celery worker starts.
imports = ('tasks.cv_task',)

# Using the database to store task state and results.
result_backend = os.environ.get('CELERY_BACKEND')

task_annotations = {'cv_task': {'rate_limit': '10/s'}}
