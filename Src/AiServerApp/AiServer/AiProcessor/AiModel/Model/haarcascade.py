from AiServer.AiProcessor.AiModel.Model.model import model
from AiServer.common.logger import _LOGGER

import cv2

class haarcascade(model):
    def __init__(self) -> None:
        haar_file = 'AiServer/AiProcessor/AiModel/Model/resources/haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(haar_file)

    def detect(self, frame) -> list:
        if frame is None:
            _LOGGER.error("No frame data")
            return None
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 4)
        detectionList = []

        for face in faces:
            detectionList.append(face.tolist())        
        return detectionList