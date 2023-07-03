package com.huy.Shared;

import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.imgcodecs.Imgcodecs;

public class helper {
    static public byte[] serializeTheImage(Mat frame){
        MatOfByte matByte = new MatOfByte();
        Imgcodecs.imencode(".jpeg", frame, matByte);
        return matByte.toArray();
    }
    static public Mat deserializeTheImage(byte[] bytes){
        MatOfByte img = new MatOfByte(bytes);
        return Imgcodecs.imdecode(img, Imgcodecs.IMREAD_COLOR);
    }
}
