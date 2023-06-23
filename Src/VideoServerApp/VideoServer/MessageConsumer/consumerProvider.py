from VideoServer.MessageConsumer.Consumer.abstractConsumer import abstractConsumer
from VideoServer.MessageConsumer.Consumer.rabbitMQConsumer import rabbitMQConsumer

def startConsumer(type, host) -> abstractConsumer:
    match type:
        case "RABBIT_MQ":
            return rabbitMQConsumer(host)
    return None