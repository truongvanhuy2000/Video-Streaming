import pika
from cameraServer.common import logger

class videoPublisher():
    def __init__(self, host) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.exchange = 'video_exchange'
        self.queue = 'metadata'

        try:
            self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
            self.channel.queue_declare(queue=self.queue, durable=True)
        except Exception:
            logger._LOGGER.error("Error when creating exchange or queue")
            exit(0)
    
    def publishToExchange(self, topic, data):
        self.channel.basic_publish(exchange=self.exchange, routing_key=topic, body=data)
    
    def publishToQueue(self, data):
        self.channel.basic_publish(exchange='', 
                                routing_key=self.queue, 
                                body=data,
                                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))

    def closeConnection(self):
        self.connection.close()
