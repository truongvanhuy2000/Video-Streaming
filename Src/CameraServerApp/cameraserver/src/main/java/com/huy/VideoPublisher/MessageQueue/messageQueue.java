package com.huy.VideoPublisher.MessageQueue;

import java.io.IOException;

public interface messageQueue {
    public String createVideoTopic(String topic);
    public String createMetadataTopic(String topic);
    public boolean publishVideo(String topic, byte[] data);
    public boolean publishMetadata(String topic, byte[] data);
    public void close();
}
