from videoServer.aiModel.Model.genericModel import genericModel
from videoServer.aiModel.Model.Yolov3 import Yolov3
from videoServer.aiModel.Model.Yolov4 import Yolov4
import os

def getModel(model):
    if not os.getenv('USE_AI'):
        pass
    match model:
        case "YOLOv4":
            return Yolov4()
        case "mobilenetssd":
            pass 
        case "YOLOv3":
            return Yolov3()
    return genericModel()