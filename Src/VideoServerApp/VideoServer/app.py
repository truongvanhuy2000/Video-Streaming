from VideoServer.MessageConsumer import consumerProvider
import  threading
import os

threadLock = threading.RLock()

def getMetadata():
    messageConsumer = consumerProvider.startConsumer(type="RABBIT_MQ", host='localhost')
    _, queue = messageConsumer.createTopic(exchange='video_exchange', 
                                                queue='metadata', 
                                                routing_key='', 
                                                binding=True, 
                                                durable=True)
    
    while True:
        data = messageConsumer.consume(topic=queue)
        if data is not None:
            threadLock.acquire()
            # -------------------------------
            # dunno.writetodatabase()
            # -------------------------------
            threadLock.release()

def run():
    getMetadata_thread = threading.Thread(target=getMetadata, daemon=True)     
    getMetadata_thread.start()