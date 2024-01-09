from typing import Dict, List
from string import ascii_letters as _base
import os, logging, random
from .. import settings


def check_path(path: str) -> bool:
    "Creating path if not exists, returns True if create"
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    return False


def generate_code(length: int = 10) -> str:
    "Generating code"
    return ''.join(random.choice(_base) for _ in range(length))


def extract_data(value: str) -> List[str]:
    "Checking value for the path and extract data or returns value"
    return [el for el in value.split('\r\n') if el.replace(' ', '')]
