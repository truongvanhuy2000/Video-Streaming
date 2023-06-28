from WebServer.Database.DB.abstractDatabase import abstractDatabase
from WebServer.common.logger import _LOGGER

import redis

class Redis(abstractDatabase):
    def __init__(self, host='localhost', port=6379, 
                 db=0, password=None, socket_timeout=None, decode_responses=True):
        if not isinstance(host, str):
            raise TypeError(f"Must provide a str, not a {type(host)}")
        if not isinstance(port, int):
            raise TypeError(f"Must provide a int, not a {type(port)}")
        
        self.redisInstance = redis.Redis(host=host, port=port, 
                                         db=db, password=password, socket_timeout=socket_timeout, decode_responses=decode_responses)
    
    def getData(self, key:str):
        if not isinstance(key, str):
            raise TypeError(f"Must provide a bool, not a {type(key)}")
        
        data = self.redisInstance.get(key)
        if data is None:
            _LOGGER.warning("This key is not exist")
        return data
    
    def isExist(self, key:str) -> bool:
        if not isinstance(key, str):
            raise TypeError(f"Must provide a bool, not a {type(key)}")
        
        if self.redisInstance.exists(key):
            return True
        return False

    def setData(self, key:str, value):
        if not isinstance(key, str):
            raise TypeError(f"Must provide a bool, not a {type(key)}")
        
        if self.isExist(key):
            _LOGGER.warning("This key is already exist, update the value")
        self.redisInstance.set(key, value) != "OK"
