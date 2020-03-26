import importlib
import os


def get_config_from_env():
    """
    从环境变量读取 config
    """
    stage = os.environ.get('STAGE')
    if stage:
        return 'configs.' + stage
    else:
        raise Exception('STAGE variable not found')


def load_config():
    return importlib.import_module(get_config_from_env())
