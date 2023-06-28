from CameraServer.common.logger import _LOGGER

import cv2
import os

class camera_server():
    def __init__(self, video) -> None:
        _LOGGER.info(video)
        self.cap = cv2.VideoCapture(video)
        if self.cap.isOpened():
            # Video is successfully opened
            _LOGGER.info("Video successfully read")
        else:
            # Failed to open the video
            _LOGGER.error("Failed to read video")
            exit()

    def readVideo(self):
        try:
            ret, frame = self.cap.read()
        except:
            _LOGGER.error("Something wrong here")
            exit(0)

        if ret == False:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        return frame
    
    def getCaptureInformation(self, parameters : list) -> dict:
        metadata = {}
        for parameter in parameters:
            match parameter:
                case 'height':
                    info = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                case 'width':
                    info = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                case 'fps':
                    info = self.cap.get(cv2.CAP_PROP_FPS)
            metadata[parameter] = info
        return metadata
    
    def isOpen(self) -> bool:
        return self.cap.isOpened()
    
    def close(self):
        self.cap.release()

