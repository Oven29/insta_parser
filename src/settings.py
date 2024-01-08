from typing import Dict
import os, logging, pathlib, json


def write_file(data: Dict[str, str]) -> None:
    with open(_settings_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))


_dir = pathlib.Path(__file__).parents[1]
_path_generator = lambda path : os.path.join(_dir, path)
_settings_file = _path_generator('settings.json')

default_values = {
    'sessions_path': _path_generator('sessions'),
    'ouput_path': _path_generator('output'),
    'logs_path': _path_generator('logs'),
    'db_path': _path_generator('database.db'),
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
DB_PATH = settings['db_path']
