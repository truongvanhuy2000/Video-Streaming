package com.huy;

import com.huy.Config.configHandler;
import com.huy.VideoPublisher.MessageQueue.messageQueue;
import com.huy.VideoReader.cv2Reader;
import org.json.JSONObject;
import org.opencv.core.Mat;

import java.io.IOException;
import java.text.MessageFormat;
import java.util.Map;

import com.huy.Shared.helper;
import static com.huy.Shared.helper.LOGGER;
import static com.huy.Config.configHandler.CONFIG;
import static com.huy.VideoPublisher.MQProvider.MessagingConfiguration;

public class App 
{
    private static final String RABBITMQ_HOST = CONFIG.getRabbitmq().get("host");
    private static final String CAMERA_NAME = "camera1";
    private static final String VIDEO_TOPIC = "video_exchange";

    private static final String METADATA_TOPIC = "metadata";

    private final messageQueue messageBroker;
    private final cv2Reader camera;
    public App(){
        try {
            messageBroker = MessagingConfiguration("RABBIT_MQ", RABBITMQ_HOST);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        camera = new cv2Reader(System.getProperty("user.dir") + "/Video/video1.mp4");
    }
    private final String createMetadata(){
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
        assert metadataTopic != null : "This should not be null";
        String videoTopic =  messageBroker.createVideoTopic(VIDEO_TOPIC);
        assert videoTopic != null : "This should not be null";

        String metadata = createMetadata();
        LOGGER.info(metadata);
        messageBroker.publishMetadata(MessageFormat.format("{0}/{1}", "", METADATA_TOPIC), metadata.getBytes());
        while (true){
            Mat frame = camera.readVideo();
            byte[] serializedFrameData = helper.serializeTheImage(frame);
//            System.out.println(serializedFrameData);
            if (!messageBroker.publishVideo(MessageFormat.format("{0}/{1}", VIDEO_TOPIC, CAMERA_NAME), serializedFrameData)){
                break;
            }
            frame.release();
        }
        camera.close();
        messageBroker.close();
    }
    public static void main(String[] args)
    {
        System.load(System.getProperty("user.dir") + "/lib/libopencv_java480.so");
        try {
            configHandler.loadConfig();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        App app = new App();
        app.serve();
    }
}
   