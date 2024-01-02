from logging.handlers import RotatingFileHandler
from typing import Tuple
import os, logging
from . import settings


def check_path(path: str) -> bool:
    "Creating path if not exists, returns True if create"
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    return False


def logging_setup(*args: Tuple[str]) -> None:
    "Logging setup"
    check_path(settings.LOGS_PATH)
    logging.basicConfig(
        handlers=(
            logging.StreamHandler(),
            RotatingFileHandler(
                filename=os.path.join(settings.LOGS_PATH, '.log'),
                mode='a',
                maxBytes=1024 * 1024,
                backupCount=4,
                encoding='utf-8',
            ),
        ),
        format='[' + ' | '.join(['%(asctime)s', '%(levelname)s'] + list(args)) + ']: %(message)s',
        datefmt='%m.%d.%Y %H:%M:%S',
        level=logging.INFO,
    )
