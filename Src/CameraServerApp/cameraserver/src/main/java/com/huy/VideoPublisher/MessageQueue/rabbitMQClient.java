package com.huy.VideoPublisher.MessageQueue;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.MessageProperties;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;


import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public final class rabbitMQClient implements messageQueue{
    private static final Logger LOGGER = LogManager.getLogger(rabbitMQClient.class);
    private Channel channel;
    private Connection connection;
    private final List<String> exchangesList = new ArrayList<>();
    private final List<String> queuesList = new ArrayList<>();
     public rabbitMQClient(String host) throws InterruptedException {
         if (host == null){
             throw new IllegalArgumentException("Host can't be null");
         }
         ConnectionFactory factory = new ConnectionFactory();
         factory.setHost(host);
         LOGGER.info(host);
         while(true){
             try{
                 connection = factory.newConnection();
                 channel = connection.createChannel();
             }
             catch(Exception e){
                 TimeUnit.SECONDS.sleep(1);
                 LOGGER.error("Can't connect to Rabbit MQ server");
                 continue;
             }
             break;
         }
         LOGGER.info("Connect success to RabbitMQ server");
     }

    @Override
    public String createVideoTopic(String topic) {
        String[] route = topic.split("/", 0);
        if (route.length < 1){
            throw new IllegalArgumentException("Wrong route format");
        }
        String exchange = route[0];

        try {
            channel.exchangeDeclare(exchange, "direct", false);
        } catch (IOException e) {
            LOGGER.error("Can't create video topic");
            System.exit(0);
        }
        exchangesList.add(exchange);
        return exchange;
    }

    @Override
    public String createMetadataTopic(String topic) {
        String[] route = topic.split("/", 0);
        if (route.length < 1){
            throw new IllegalArgumentException("Wrong route format");
        }
        String queue = route[0];
        String queueName = "";
        try {
            queueName = channel.queueDeclare(queue, true, false, false, null).getQueue();
        } catch (IOException e) {
            LOGGER.error("Can't create video topic");
            System.exit(0);
        }
        queuesList.add(queueName);
        return queueName;
    }

    @Override
    public boolean publishVideo(String topic, byte[] data)
    {
        return publish(topic, data);
    }
    @Override
    public boolean publishMetadata(String topic, byte[] data)
    {
        return publish(topic, data);
    }

    private boolean publish(String topic, byte[] data){

        String[] route = topic.split("/", 0);
        if (route.length < 2){
            LOGGER.error("Wrong topic format");
            return false;
        }

        String exchange = route[0];
        String routing_key = route[1];

        try {
            channel.basicPublish(exchange, routing_key, MessageProperties.PERSISTENT_BASIC, data);
        } catch (IOException e) {
            LOGGER.error("Can't publish metadata");
            return false;
        }
        return true;
    }
    @Override
    public void close() {
         exchangesList.forEach(exchange ->{
             try {
                 channel.exchangeDelete(exchange);
             } catch (IOException e) {
                 LOGGER.error("Exception when delete exchange:", e);
             }
         });
         queuesList.forEach(queue -> {
             try{
                 channel.queueDelete(queue);
             } catch (IOException e) {
                 LOGGER.error("Exception when delete queue:", e);
             }
         });
        try {
            channel.close();
            connection.close();
        } catch (Exception e) {
            LOGGER.error("Exception when close channel:", e);
        }
    }
}
