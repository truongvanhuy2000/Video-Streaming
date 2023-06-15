from videoServer.aiModel import modelProvider
from videoServer.common import logger

import cv2
import os

VIDEO_DIRECTORY = os.getenv('RESOURCE_DIR')
if VIDEO_DIRECTORY is None:
    logger._LOGGER.error("Missing env")
    exit()

class camera_server():
    def __init__(self, video, model) -> None:
        dir = VIDEO_DIRECTORY + video + '.mp4'
        logger._LOGGER.info(f"Open video from directory: {dir}")
        self.cap = cv2.VideoCapture(dir)
        # self.AImodel = modelProvider.getModel(model)
        if self.cap.isOpened():
            # Video is successfully opened
            logger._LOGGER.info("Video successfully read")
        else:
            # Failed to open the video
            logger._LOGGER.error("Failed to read video")
            exit()

    def humanDetect(self):
        try:
            ret, frame = self.cap.read()
        except:
            logger._LOGGER.error("something wrong here")
        if ret == False:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        # self.AImodel.detect(frame)
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
        return frame
    
    def isOpen(self) -> bool:
        return self.cap.isOpened()
    
    def close(self):
        self.cap.release()