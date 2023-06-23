from VideoServer.MessageConsumer.Consumer.abstractConsumer import abstractConsumer
from VideoServer.common import logger

import pika

class rabbitMQConsumer(abstractConsumer):
    def __init__(self, host) -> None:
        self.host = host

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()

        self.exchanges = []
        self.queues = []
    
    def createTopic(self, **kwargs):
        if kwargs.get('exchange') is not None: 
            exchange = self.createExchange(self, kwargs.get('exchange'), kwargs)
            self.exchanges.append(exchange)

        if kwargs.get('queue') is not None:
            queue = self.createQueue(self, kwargs.get('queue'), kwargs)
            self.queues.append(queue)

        # Binding queue with exchange if needed
        if kwargs.get('binding') == True and any in [exchange, queue] is not None:
            self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=kwargs.get('routing_key'))

        return (exchange, queue)

    def createQueue(self, queue, **kwargs):
        durable = True if kwargs.get('durable') is True else False
        exclusive = True if kwargs.get('exclusive') is True else False
        try:
            createdQueue = self.channel.queue_declare(queue=queue, durable=durable, exclusive=exclusive).method.queue
        except Exception:
            logger._LOGGER.error(f"Error when creating queue")
            return None
        
        self.queues.append(queue)
        return createdQueue

    def createExchange(self, exchange, **kwargs):
        exchange_type = None if kwargs.get('exchange_type') is None else kwargs.get('exchange_type')
        durable = True if kwargs.get('durable') is True else False

        try:
            self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=durable)
        except Exception:
            logger._LOGGER.error("Error when creating exchange")
            return None

        self.exchanges.append(exchange)
        return exchange

    def consume(self, topic):
        # Fair dispatch
        self.channel.basic_qos(prefetch_count=1)

        method_frame, header_frame, body = self.channel.basic_get(topic)
        if body is None:
            return None
        
        # Acknowledge the message
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return body
    
    def closeConnection(self):
        for exchange in self.exchanges:
            self.channel.exchange_delete(exchange)
            self.exchanges.pop(exchange)

        for queue in self.queues:
            self.channel.queue_delete(queue)
            self.queues.pop(queue)
        
        self.channel.close()
        self.connection.close()




            


        