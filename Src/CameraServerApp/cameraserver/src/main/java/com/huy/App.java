package com.huy;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.opencv.videoio.VideoCapture;
import org.opencv.videoio.Videoio;
import org.opencv.core.Mat;

import java.awt.image.*;
import java.util.Objects;
import javax.swing.*;

//import static com.huy.Shared.logger.LOGGER;
/**
 * Hello world!
 *
 */
public class App 
{
    public static final Logger LOGGER = LogManager.getLogger(App.class);

    public void displayVideo() {
        String videoPath = "";
        try {
            videoPath = Objects.requireNonNull(getClass().getResource("/Video/video1.mp4")).getPath();
        }
        catch(Exception e){
            System.out.println("Exception type: " + e.getClass().getName());
        }
        if (videoPath.equals("")) {
            System.out.println("Can't find video path");
            return;
        }
        VideoCapture camera = new VideoCapture(videoPath, Videoio.CAP_FFMPEG);
        if (!camera.isOpened()) {
            LOGGER.error("Open video failed");
        }
        LOGGER.info("Open video success");
    }
    public static void main(String[] args)
    {
        System.load("/home/huy/opencv-4.8.0/build/lib/libopencv_java480.so");
        System.out.println( "Hello World!" );
        App app = new App();
        app.displayVideo();
    }
}
   