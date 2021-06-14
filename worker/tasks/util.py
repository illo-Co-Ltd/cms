import errno
import os
import signal
import time
from collections.abc import Iterable
import pathlib
import xml.etree.ElementTree as ETree
from functools import wraps

import celery
import requests
from celery.utils.log import get_task_logger
from requests.auth import HTTPDigestAuth


def refine_path(path):
    return str(pathlib.Path(path))


def check_and_create(dirname):
    if os.path.isdir(dirname):
        return True
    else:
        try:
            os.mkdir(dirname)
            return True
        except FileNotFoundError:
            check_and_create(os.path.dirname(dirname))
            os.mkdir(dirname)
            return True
        except Exception as e:
            raise e


def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes, celery.canvas.Signature)):
            yield from flatten(el)
        else:
            yield el

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL,seconds) #used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator

@timeout(10)
def is_stopped(device, x, y, z):
    logger = get_task_logger(__name__)
    while True:
        resp = requests.get(
            f'http://{device.ip}/isp/st_d100.xml',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            return False
        resp.encoding = None
        tree = ETree.fromstring(resp.text)
        d100 = tree.find('D100')
        curx = int(d100.find('CURX').text)
        cury = int(d100.find('CURY').text)
        curz = int(d100.find('CURZ').text)
        if curx==x and cury==y and curz==z:
            return True
        else:
            logger.info(f'curx:<{curx}>  cury:<{cury}>  curz:<{curz}')
            logger.info(f'tgtx:<{x}>  tgty:<{y}>  tgtz:<{z}')
            time.sleep(0.5)


def autofocus(device):
    resp = requests.get(
        f'http://{device.ip}/isp/appispmu.cgi?i_c1_dirafc=+run+',
        auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
    )
    if resp.status_code == 200:
        return True
    else:
        return False
