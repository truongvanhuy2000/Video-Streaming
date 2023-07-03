package com.huy.VideoReader;

import com.huy.App;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.opencv.core.Size;
import org.opencv.videoio.VideoCapture;
import org.opencv.videoio.Videoio;
import org.opencv.imgproc.Imgproc;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

import java.util.HashMap;

public class cv2Reader {
    public static final Logger LOGGER = LogManager.getLogger(cv2Reader.class);
    private final VideoCapture cap;
    public cv2Reader(String filename){
        cap = new VideoCapture(filename, Videoio.CAP_FFMPEG);
        if (!cap.isOpened()){
            LOGGER.error("Open video failed");
            System.exit(0);
        }
        LOGGER.info("Open video success");
    }

    public final Mat readVideo(){
        Mat frame = new Mat();
        if (!cap.read(frame)){
            cap.set(Videoio.CAP_PROP_POS_FRAMES, 0);
            cap.read(frame);
        }
        Mat resizedFrame = new Mat();
        Imgproc.resize(frame, resizedFrame, new Size(), 0.5, 0.5, Imgproc.INTER_AREA);
        return resizedFrame;
    }

    public HashMap<String, String> getCaptureInformation(String... args){
        HashMap<String, String> metadata = new HashMap<>();
        String info = "";
        for (String arg : args){
            switch (arg){
                case "height":
                    info = Double.toString(cap.get(Videoio.CAP_PROP_FRAME_HEIGHT));
                    break;
                case "width":
                    info = Double.toString(cap.get(Videoio.CAP_PROP_FRAME_WIDTH));
                    break;
                case "fps":
                    info = Double.toString(cap.get(Videoio.CAP_PROP_FPS));
                    break;
                default:
                    break;
            }
            metadata.put(arg, info);
        }
        return  metadata;
    }

    public final void close(){
        cap.release();
    }
}