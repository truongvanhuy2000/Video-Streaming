from VideoServer.Transportation.Protocol.abstractProtocol import abstractProtocol
from VideoServer.Transportation.Protocol.httpProtocol import httpProtocol

def getTransportMethod(method, host, port) -> abstractProtocol:
    match method:
        case "GRPC":
            pass
        case "HTTP":
            return httpProtocol(host, port)
        case "other":
            pass
    