from AiServer.AiProcessor.AiModel.Model.model import model
from AiServer.AiProcessor.AiModel.Model.haarcascade_smile import haarcascade_smile
from AiServer.AiProcessor.AiModel.Model.haarcascade_frontalface import haarcascade_frontalface

def getModel(model) -> model:
    match model:
        case "haarcascade_frontalface":
            return haarcascade_frontalface()
        case "haarcascade_smile":
            return haarcascade_smile()
    return None