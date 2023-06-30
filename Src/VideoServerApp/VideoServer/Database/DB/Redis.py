from VideoServer.Database.DB.abstractDatabase import abstractDatabase
from VideoServer.common.logger import _LOGGER

import redis

class Redis(abstractDatabase):
    def __init__(self, host='localhost', port=6379, 
                 db=0, password=None, socket_timeout=None, decode_responses=True):
        
        self.redisInstance = redis.Redis(host=host, port=port, 
                                         db=db, password=password, socket_timeout=socket_timeout, decode_responses=decode_responses)
    
    def getData(self, key):
        data = self.redisInstance.get(key)
        if data is None:
            _LOGGER.warning("This key is not exist")
        return data
    
    def isExist(self, key) -> bool:
        if self.redisInstance.exists(key):
            return True
        return False

    def setData(self, key, value):
        if self.isExist(key):
            _LOGGER.warning("This key is already exist, update the value")
        self.redisInstance.set(key, value) != "OK"

    def getAll(self, filter=None):
        match = '*'
        returnList = []
        if filter != None:
            match = f"{filter}*"
        for key in self.redisInstance.scan_iter(match):
            returnList.append(key.decode())
            
        return returnList
