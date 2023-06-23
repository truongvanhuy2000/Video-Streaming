from AiServer.AiProcessor.AiModel.Model.model import model
from AiServer.AiProcessor.AiModel.Model.haarcascade import haarcascade

def getModel(model) -> model:
    match model:
        case "haarcascade_frontalface":
            return haarcascade()
        case "mobilenetssd":
            pass 

        case "YOLOv3":
            pass

    return None