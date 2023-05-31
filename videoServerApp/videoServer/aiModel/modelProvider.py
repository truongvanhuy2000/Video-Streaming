from videoServer.aiModel.Model.genericModel import genericModel
from videoServer.aiModel.Model.Yolov3 import Yolov3
from videoServer.aiModel.Model.Yolov4 import Yolov4

def getModel(model):
    # match model:
    #     case "YOLOv4":
    #         return Yolov4()
    #     case "mobilenetssd":
    #         pass 
    #     case "YOLOv3":
    #         return Yolov3()
    return genericModel()