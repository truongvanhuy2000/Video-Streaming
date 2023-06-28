from AiServer.AiProcessor.AiModel import modelProvider
from AiServer.common.logger import _LOGGER
from AiServer.common import helper

import json

class faceDetection():
    def __init__(self, model) -> None:
        self.detectionModel = modelProvider.getModel(model)
        if self.detectionModel == None:
            _LOGGER.error('This detection model is not exist')
        
    def detect(self, frame):
        frame = helper.deserializeTheImage(frame)
        detections = self.detectionModel.detect(frame)
        if len(detections) == 0:
            return None
        
        detections = {
            'faces' : detections
        }
        try:
            detections = json.dumps(detections)
        except TypeError as e:
            _LOGGER.error(f"There error with this json dumps: {e}")
            return None
        
        _LOGGER.debug(detections)
        return detections
