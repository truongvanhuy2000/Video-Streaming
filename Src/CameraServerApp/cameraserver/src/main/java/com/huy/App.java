package com.huy;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.opencv.videoio.VideoCapture;
import org.opencv.videoio.Videoio;
import org.opencv.core.Mat;

import java.awt.image.*;
import java.util.Objects;
import javax.swing.*;

import com.huy.Shared.helper;
/**
 * Hello world!
 *
 */
public class App 
{
    public static final Logger LOGGER = LogManager.getLogger(App.class);

    public void displayVideo() {
        String videoPath = helper.getResources("/Video/video1.mp4");
        VideoCapture camera = new VideoCapture(videoPath, Videoio.CAP_FFMPEG);
        if (!camera.isOpened()) {
            LOGGER.error("Open video failed");
        }
        LOGGER.info("Open video success");
    }
    public static void main(String[] args)
    {
        System.loadLibrary("libopencv_java480.so");
        System.out.println( "Hello World!" );
        App app = new App();
        app.displayVideo();
    }
}
   