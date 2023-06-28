from VideoServer.MessageConsumer import consumerProvider
from VideoServer.common.logger import _LOGGER
from VideoServer.Database import databaseProvider
from VideoServer.Service import httpServer
from VideoServer.Config.config import CONFIG
import  threading
import json

# Configuration for connection to database
DATABASE_TYPE = CONFIG.database_type
DATABASE_HOST = CONFIG.database_host
DATABASE_PORT = CONFIG.database_port
# Configuration for connection to rabbitmq
RABBITMQ_HOST = CONFIG.rabbitmq_host

threadLock = threading.RLock()

def parseMetadata(metadata):
    metadata = json.loads(metadata)
    key = metadata.get('camera')
    value = metadata.get('metadata')

    if any(item is None for item in [key, value]):
        _LOGGER.error("Cant parse this metadata: Missing key/value")
        return None, None
    
    return key, json.dumps(value)

def getMetadata():
    _LOGGER.info("Get Metadata thread is running")

    messageConsumer = consumerProvider.startConsumer(type="RABBIT_MQ", 
                                                     host=RABBITMQ_HOST)
    
    _, queue = messageConsumer.createTopic(exchange='video_exchange', 
                                            exchange_type = 'direct',
                                            queue='metadata', 
                                            durable=True)
    
    if queue is None:
        _LOGGER.error("Cant create topic")
        return
    
    database = databaseProvider.getDatabase(type=DATABASE_TYPE, 
                                            host=DATABASE_HOST, 
                                            port=DATABASE_PORT, 
                                            db=0)
    
    while True:
        data = messageConsumer.consume(topic=queue)
        if data is None:
            continue
        
        _LOGGER.info(data)
        key, value = parseMetadata(data)

        if any(item is None for item in [key, value]):
            continue

        threadLock.acquire()
        database.setData(key, value)
        threadLock.release()

def run():
    getMetadata_thread = threading.Thread(target=getMetadata, daemon=True)     
    getMetadata_thread.start()
    httpServer_thread = threading.Thread(target=httpServer.serve())
    httpServer_thread.start()

    httpServer_thread.join()