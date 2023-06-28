from VideoServer.MessageConsumer.Consumer.abstractConsumer import abstractConsumer
from VideoServer.common.logger import _LOGGER

import pika
import time

class rabbitMQConsumer(abstractConsumer):
    def __init__(self, host) -> None:
        self.host = host
        while True:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
            except Exception as e:
                time.sleep(1)
                continue
            break
        _LOGGER.info(f"Connect to Rabbit MQ at {host}")
        self.channel = self.connection.channel()

        self.exchanges = []
        self.queues = []
    
    def createTopic(self, **kwargs):
        if kwargs.get('exchange') is not None: 
            exchange = self.createExchange(exchange=kwargs.get('exchange'), kwargs=kwargs)
            self.exchanges.append(exchange)

        if kwargs.get('queue') is not None:
            queue = self.createQueue(queue=kwargs.get('queue'), kwargs=kwargs)
            self.queues.append(queue)

        # Binding queue with exchange if needed
        if kwargs.get('binding') == True and any(item is not None for item in [exchange, queue]):
            routing_key = kwargs.get('routing_key', '')
            _LOGGER.debug(f"Binding with {routing_key}")
            self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

        return (exchange, queue)

    def createQueue(self, queue, **kwargs):
        durable = kwargs.get('durable', True)
        exclusive = kwargs.get('exclusive', False)
        
        try:
            createdQueue = self.channel.queue_declare(queue=queue, durable=durable, exclusive=exclusive).method.queue
            _LOGGER.debug(f"Queue created: {createdQueue}")
        except Exception as e:
            _LOGGER.error(f"Error when creating queue {e}")
            return None
        
        self.queues.append(queue)
        return createdQueue

    def createExchange(self, exchange, **kwargs):
        exchange_type = kwargs.get('exchange_type', 'direct')

        try:
            self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        except Exception as e:
            _LOGGER.error(f"Error when creating exchange {e}")
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
        #This is still a unsolved problem -------------------------------------------------------

        # for exchange in self.exchanges:
        #     self.channel.exchange_delete(exchange, if_unused=True)
        # self.exchanges.clear()

        #This is still a unsolved problem -------------------------------------------------------
        
        for queue in self.queues:
            self.channel.queue_delete(queue)

        self.queues.clear()
        self.connection.close()




            


        