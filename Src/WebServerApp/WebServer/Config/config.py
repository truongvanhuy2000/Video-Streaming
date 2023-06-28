import os
from os.path import join
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
    def website_host(self):
        return self._config['website']['host']
    
    @property
    def website_port(self):
        return self._config['website']['port']
    
    @property
    def loadbalancer_host(self):
        return self._config['loadbalancer']['host']
    
    @property
    def loadbalancer_port(self):
        return self._config['loadbalancer']['port']
    
    @property
    def loadbalancer_transport_method(self):
        return self._config['loadbalancer']['transport']['method']
    
    @property
    def loadbalancer_transport_timeout(self):
        return self._config['loadbalancer']['transport']['timeout']
    
    @property
    def database_host(self):
        return self._config['database']['host']
    
    @property
    def database_port(self):
        return self._config['database']['port']
    
    @property
    def database_type(self):
        return self._config['database']['type']
    
    @property
    def logging_level(self):
        return self._config['logging']['level']

CONFIG = _Config()