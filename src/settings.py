import os, logging, pathlib


# paths
_dir = pathlib.Path(__file__).parents[1]

SESSIONS_PATH = os.path.join(_dir, 'sessions')
LOGS_PATH = os.path.join(_dir, 'logs')
LOG_LEVEL = logging.INFO
