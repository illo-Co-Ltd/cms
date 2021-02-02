import celery

from .taskmanager import celery_app
from util import logger



def capture_send(header: str, data: dict):
    name = 'cam_task.capture_task'
    task = celery_app.send_task(name, args=[header, data])
    return task.id


def start_timelapse_send(header: str, run_every: float, expire_at: str, data: dict):
    from redbeat import RedBeatSchedulerEntry
    interval = celery.schedules.schedule(run_every=run_every)  # seconds
    entry = RedBeatSchedulerEntry(
        'timelapse',
        'cam_task.capture_task',
        interval,
        args=[header, data],
        app=celery_app
    )
    entry.save()
    return True, entry.key
    # task = celery_app.send_task('cam_task.start_timelapse_task', args=[header, run_every, expire_at, data])
    return task.get()


def stop_timelapse_send(key):
    task = celery_app.send_task('cam_task.stop_timelapse_task', args=[key])
    return task.get()
