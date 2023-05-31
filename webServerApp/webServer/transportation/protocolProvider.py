import os
from webServer.transportation.protocol.grpcClient import grpcClient
from webServer.transportation.protocol.httpClient import httpClient

def getTransportMethod(method):
    match method:
        case "GRPC":
            return grpcClient()
        
        case "HTTP":
            return httpClient()

        case "other":
            pass
    
        

    
    