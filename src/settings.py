import os, pathlib, dotenv


_dir = pathlib.Path(__file__).parents[1]
config_path = os.path.join(_dir, 'settings.conf')
if os.path.exists(config_path):
    dotenv.load_dotenv(config_path)

# paths
SESSIONS_PATH = os.path.join(_dir, 'sessions')
LOGS_PATH = os.path.join(_dir, 'logs')
