import pika
from CameraServer.common import logger

class videoPublisher():
    def __init__(self, host) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()

        self.exchanges = []
        self.queues = []

    def createQueue(self, queue, durable=False):
        try:
            self.channel.queue_declare(queue=queue, durable=durable)
        except Exception:
            logger._LOGGER.error("Error when creating queue")
            return
        
        self.queues.append(queue)
        
    def createExchange(self, exchange, exchange_type='direct', durable=False):
        try:
            self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=durable)
        except Exception:
            logger._LOGGER.error("Error when creating exchange")
            return

        self.exchanges.append(exchange)

    def publish(self, exchange='', routing_key='', data=None, persistent=False):
        properties = pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE) if persistent == True else None
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=data, properties=properties)
    
    def closeConnection(self):
        self.connection.close()
        for exchange in self.exchanges:
            self.channel.exchange_delete(exchange)
            self.exchanges.pop(exchange)

        for queue in self.queues:
            self.channel.queue_delete(queue)
            self.queues.pop(queue)
        
