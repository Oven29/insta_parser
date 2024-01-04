from logging.handlers import RotatingFileHandler
from typing import Tuple, Dict, List
from string import ascii_letters as _base
import os, logging, random
from . import settings


def check_path(path: str) -> bool:
    "Creating path if not exists, returns True if create"
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    return False


def generate_code(length: int = 10) -> str:
    "Generating code"
    return ''.join(random.choice(_base) for _ in range(length))


def logging_setup(*args: Tuple[str]) -> None:
    "Logging setup"
    check_path(settings.LOGS_PATH)
    logging.basicConfig(
        handlers=(
            logging.StreamHandler(),
            RotatingFileHandler(
                filename=os.path.join(settings.LOGS_PATH, f'{generate_code()}.log'),
                mode='w',
                encoding='utf-8',
            ),
        ),
        format='[' + ' | '.join(['%(asctime)s', '%(levelname)s'] + list(args)) + ']: %(message)s',
        datefmt='%m.%d.%Y %H:%M:%S',
        level=settings.LOG_LEVEL,
    )


def get_sessions() -> Dict[str, str]:
    "Returns dictionary of usernames and paths to session files these username"
    sessions = {}
    for filename in list(os.walk(settings.SESSIONS_PATH))[0][2]:
        username, extension = filename.rsplit('.', 1)
        if extension == 'session':
            sessions[username] = os.path.join(settings.SESSIONS_PATH, filename)
    return sessions


def extract_data(value: str) -> List[str]:
    "Checking value for the path and extract data or returns value"
    if os.path.exists(value):  # path to file with data
        with open(value, 'r', encoding='utf-8') as f:
            data = f.read().split('\n')
            return [el for el in data if el.replace(' ', '')]
    return [value]
