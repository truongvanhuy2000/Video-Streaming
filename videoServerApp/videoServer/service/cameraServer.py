from videoServer.aiModel import modelProvider
from videoServer.common import logger

import cv2
import os

class camera_server():
    def __init__(self, video, model) -> None:
        dir = os.getenv('RESOURCE_DIR') + video + '.mp4'
        self.cap = cv2.VideoCapture(dir)
        # self.AImodel = modelProvider.getModel(model)
    
    def humanDetect(self):
        try:
            ret, frame = self.cap.read()
        except:
            logger._LOGGER.error("something wrong here")
        if ret == False:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        # self.AImodel.detect(frame)
        return frame
    
    def isOpen(self) -> bool:
        return self.cap.isOpened()
    
    def close(self):
        self.cap.release()