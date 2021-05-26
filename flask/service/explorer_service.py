import os
import traceback

from util.logger import logger


def listdir(dirpath):
    logger.info('listing files and directories in specific directory.')
    try:
        return os.listdir(f'/data/{dirpath}')

    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
