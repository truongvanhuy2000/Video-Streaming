from videoServer.transportation.grpcServer import grpcServer
from videoServer.transportation.httpServer import httpServer

def getProtocol(protocol):
    match protocol:
        case "GRPC":
            return grpcServer()
        case "HTTP":
            return httpServer()
        case "SFTP":
            pass
    return grpcServer()