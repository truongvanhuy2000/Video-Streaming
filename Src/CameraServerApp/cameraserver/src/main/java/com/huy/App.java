package com.huy;

import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.video.Video;
import org.opencv.videoio.VideoCapture;

/**
 * Hello world!
 *
 */
public class App 
{
    public void displayVideo()
    {
        String videoPath = "/home/huy/Videos/video1.mp4";
//        try {
//            videoPath =
//            videoPath = getClass().getResource("/Video/video1.mp4").getPath();
//            System.out.println(videoPath);
//        }
//        catch(Exception e){
//            System.out.println("Exception type: " + e.getClass().getName());
//        }
//        if (videoPath.equals("")) {
//            System.out.println("Can't find video path");
//            return;
//        }
        VideoCapture camera = new VideoCapture(videoPath);
        if (!camera.isOpened())
        {
            System.out.println("Open video failed");
        }
    }
    public static void main( String[] args )
    {
        System.load("/home/huy/githubRepo/opencv-4.8.0/build/lib/libopencv_java480.so");
        System.out.println( "Hello World!" );
        App app = new App();
        app.displayVideo();
    }
}
   