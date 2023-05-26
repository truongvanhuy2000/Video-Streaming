from videoServer.common import helper

import cv2
import os

class camera_server():
    def __init__(self, video, model) -> None:
        dir = 'videoServer/resources/' + video + '.mp4'
        self.cap = cv2.VideoCapture(dir)
        self.AImodel = self.getModel(model)

    def getModel(self, model):
        match model:
            case "YOLOv4":
                return self.YOLOv4Model()
            case "mobilenetssd":
                return self.mobilenetssdModel()
            case "YOLOv3":
                return self.YOLOv3Model()
        return self.genericModel()
    
    def humanDetect(self):
        # Display the resulting frame
        # initialize the HOG descriptor
        try:
            ret, frame = self.cap.read()
        except:
            print("something wrong here")
        if ret == False:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        # detect humans in input image
        # (humans, _) = self.AImodel.detectMultiScale(frame, winStride=(10, 10), padding=(32, 32), scale=1.1)
        # # loop over all detected humans
        # for (x, y, w, h) in humans:
        #     pad_w, pad_h = int(0.15 * w), int(0.01 * h)
        #     cv2.rectangle(frame, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), 2)
        return frame
    
    def YOLOv4Model(self):
        pass

    def mobilenetssdModel(self):
        pass
    
    def YOLOv3Model(self):
        pass
    # return a generic model that is built into opencv
    def genericModel(self):
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        return hog
        
    def isOpen(self) -> bool:
        return self.cap.isOpened()
    def close(self):
        self.cap.release()