package com.huy;

import com.huy.Config.configHandler;
import com.huy.VideoPublisher.MessageQueue.messageQueue;
import com.huy.VideoReader.cv2Reader;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;
import org.opencv.core.Mat;

import java.io.IOException;
import java.text.MessageFormat;
import java.util.Map;

import com.huy.Shared.helper;
import static com.huy.Config.configHandler.CONFIG;
import static com.huy.VideoPublisher.MQProvider.MessagingConfiguration;

public class App 
{
    public static void main(String[] args)
    {
        System.load(System.getProperty("user.dir") + "/lib/libopencv_java480.so");
        configHandler.loadConfig();
        cameraServer camera = new cameraServer();
        camera.serve();
    }
}
class cameraServer{
    private static final Logger LOGGER = LogManager.getLogger(App.class);
    private static final String RABBITMQ_HOST = CONFIG.getRabbitmq().get("host");
    private static final String CAMERA_NAME = "camera1";
    private static final String VIDEO_TOPIC = "video_exchange";
    private static final String METADATA_TOPIC = "metadata";
    private final messageQueue messageBroker;
    private final cv2Reader camera;
    public cameraServer(){
        try {
            messageBroker = MessagingConfiguration("RABBIT_MQ", RABBITMQ_HOST);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        camera = new cv2Reader(System.getProperty("user.dir") + "/Video/video1.mp4");
    }
    private String createMetadata(){
        Map<String, String> metadata = camera.getCaptureInformation("height", "width", "fps");
        metadata.put("exchange", VIDEO_TOPIC);
        metadata.put("topic", CAMERA_NAME);

        JSONObject cameraInfo = new JSONObject();
        cameraInfo.put("camera", CAMERA_NAME);
        cameraInfo.put("metadata", metadata);
        return cameraInfo.toString();
    }
    public final void serve() {
        String metadataTopic = messageBroker.createMetadataTopic(METADATA_TOPIC);
        String videoTopic =  messageBroker.createVideoTopic(VIDEO_TOPIC);

        String metadata = createMetadata();
        String metadataRoute = MessageFormat.format("{0}/{1}", "", metadataTopic);
        if (!messageBroker.publishMetadata(metadataRoute, metadata.getBytes())){
            LOGGER.error("Can't publish metadata to broker");
            return;
        }
        while (true){
            Mat frame = camera.readVideo();
            byte[] serializedFrameData = helper.serializeTheImage(frame);
            String videoRoute = MessageFormat.format("{0}/{1}", videoTopic, CAMERA_NAME);
            if (!messageBroker.publishVideo(videoRoute, serializedFrameData)){
                break;
            }
            frame.release();
        }
        camera.close();
        messageBroker.close();
    }
}
   