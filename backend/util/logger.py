import logging

"""
    Set Default Formatter
"""
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')

"""
    Set My Loogger
"""

logger = logging.getLogger('MY_FLASK_LOG')
logger.setLevel(logging.DEBUG)
stream_log = logging.StreamHandler()
stream_log.setFormatter(formatter)
logger.addHandler(stream_log)
# 로그 disabled
# my_logger.disabled = True