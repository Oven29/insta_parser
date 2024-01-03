from typing import Dict
import os, logging, pathlib, json


def write_file(data: Dict[str, str]) -> None:
    with open(_settings_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))


_dir = pathlib.Path(__file__).parents[1]
_settings_file = os.path.join(_dir, 'settings.json')
default_values = {
    'sessions_path': os.path.join(_dir, 'sessions'),
    'ouput_path': os.path.join(_dir, 'output'),
    'logs_path': os.path.join(_dir, 'logs'),
    'log_level': 'info',
}
if os.path.exists(_settings_file):
    with open(_settings_file, 'r', encoding='utf-8') as f:
        settings = json.loads(f.read())
else:
    settings = default_values
    write_file(settings)


def update_settings(key: str, value: str) -> None:
    settings[key] = value
    write_file(settings)


SESSIONS_PATH = settings['sessions_path']
OUTPUT_PATH = settings['ouput_path']
LOGS_PATH = settings['logs_path']
LOG_LEVEL = logging._nameToLevel.get(settings['log_level'])
