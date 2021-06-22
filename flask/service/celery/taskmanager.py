import re
import traceback
import json

from celery import Celery
import redis

from service.celery import celeryconfig
import redbeat
from util.logger import logger

celery_app = Celery('worker')
celery_app.config_from_object(celeryconfig)
rd0 = redis.StrictRedis(host='redis', port=6379, db=0, charset='utf-8', decode_responses=True)
rd1 = redis.StrictRedis(host='redis', port=6379, db=1, charset='utf-8', decode_responses=True)


def list_all_tasks(serial):
    i = celery_app.control.inspect()
    logger.info(i.scheduled())
    logger.info(i.active())
    logger.info(i.reserved())

def list_schedule():
    try:
        logger.info(f'Listing all schedules')
        return rd1.zrange('redbeat::schedule', 0, -1)
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def get_schedule(serial):
    try:
        logger.info(f'Fetching schedule for device<{serial}>')
        schedules = rd1.zrange('redbeat::schedule', 0, -1)
        match = [s if re.search(f'<device {serial}>', s) else None for s in schedules]
        match = list(filter(None, match))
        if len(match) > 0:
            htable = rd1.hgetall(match[0])
            ret = {k: json.loads(v) for k, v in htable.items()}
            return ret
        else:
            return None

    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def delete_schedule(serial):
    try:
        logger.info(f'Deleting schedule for device<{serial}>')
        schedules = rd1.zrange('redbeat::schedule', 0, -1)
        match = [s if re.search(f'<device {serial}>', s) else None for s in schedules]
        match = list(filter(None, match))
        if len(match) > 0:
            logger.info(f'match[0]: {match[0]}')
            redbeat.RedBeatSchedulerEntry.from_key(match[0], app=celery_app).delete()
            from redbeat import schedulers
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
