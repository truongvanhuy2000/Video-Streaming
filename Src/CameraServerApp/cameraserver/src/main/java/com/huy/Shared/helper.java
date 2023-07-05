package com.huy.Shared;

import com.huy.App;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.imgcodecs.Imgcodecs;

import java.io.InputStream;
import java.net.URL;

public class helper {
     static public byte[] serializeTheImage(Mat frame){
        MatOfByte matByte = new MatOfByte();
        Imgcodecs.imencode(".jpg", frame, matByte);
        return matByte.toArray();
    }
    static public Mat deserializeTheImage(byte[] bytes){
        MatOfByte img = new MatOfByte(bytes);
        return Imgcodecs.imdecode(img, Imgcodecs.IMREAD_COLOR);
    }

    static public InputStream getResources(String path){
        InputStream resourceAbsolutePath = helper.class.getClassLoader().getResourceAsStream(path);
        if (resourceAbsolutePath == null) {
            throw new IllegalArgumentException("file not found! " + path);
        } else {
            return resourceAbsolutePath;
        }
    }
}
