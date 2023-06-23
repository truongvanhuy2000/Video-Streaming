from AiServer.AiProcessor.AiModel import modelProvider
from AiServer.common import logger
from AiServer.common import helper

import json

class faceDetection():
    def __init__(self, model) -> None:
        self.detectionModel = modelProvider.getModel(model)
        if self.detectionModel == None:
            logger._LOGGER.error('This detection model is not exist')
        
    def detect(self, frame):
        frame = helper.deserializeTheImage(frame)
        detections = self.detectionModel.detect(frame)
        if len(detections) == 0:
            return None
        detections = json.dumps(detections)
        
        logger._LOGGER.debug(detections)
        return json.dumps(detections)
