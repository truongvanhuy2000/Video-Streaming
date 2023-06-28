import os
from os.path import dirname, join
import sys
import yaml
import pathlib


_global_configpath = join(pathlib.Path(__file__).parent.resolve(), "yaml/config.yaml")


def get_configpath() -> str:
    if os.path.exists(_global_configpath):
        
        return _global_configpath

def get_config() -> dict:
    with open(get_configpath(), 'rt') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


class _Config:
    
    def __init__(self):
        """This method is defined to remind you that this is not a static class"""
        self._config = get_config()

    @property
    def camera_name(self):
        return os.getenv('CAMERA_NAME')
    
    @property
    def rabbitmq_host(self):
        return self._config['rabbitmq']['host']

    @property
    def resource(self):
        return os.getenv('RESOURCE')
    
    @property
    def logging_level(self):
        return self._config['logging']['level']

CONFIG = _Config()