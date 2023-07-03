package com.huy.VideoPublisher;
import com.huy.VideoPublisher.MessageQueue.messageQueue;
import com.huy.VideoPublisher.MessageQueue.rabbitMQClient;

public class MQProvider {
    public static messageQueue MessagingConfiguration(String type, String host) throws InterruptedException {
        switch (type){
            case "RABBIT_MQ":
                return new rabbitMQClient(host);
            case "KAFKA":
                // Cause i haven't implement this yet
                return null;
            default:
                return null;
        }
    }
}
