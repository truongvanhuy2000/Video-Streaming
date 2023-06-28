from VideoServer.Database.DB.abstractDatabase import abstractDatabase
from VideoServer.Database.DB.Redis import Redis

def getDatabase(type, host, port, **kwargs) -> abstractDatabase:
    match type:
        case "REDIS":
            return Redis(host=host, port=port, 
                         db=kwargs.get('db', 0),
                         password=kwargs.get('password', None),
                         socket_timeout=kwargs.get('socket_timeout' ,None),
                         decode_responses=kwargs.get('decode_responses' ,False))
    
        case "SOMETHING_ELSE":
            pass