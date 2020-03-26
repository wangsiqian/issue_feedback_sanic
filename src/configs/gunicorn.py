import importlib

from app import app
from configs.loader import get_config_from_env

config = get_config_from_env()
config_object = importlib.import_module(config)
app.config.from_object(config_object)

bind = '0.0.0.0:8000'

workers = 3
max_requests = 3000
max_requests_jitter = 1000
