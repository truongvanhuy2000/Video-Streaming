import os
from webServer.transportation.grpcClient import grpcClient
from webServer.transportation.httpClient import httpClient

def getTransportMethod(method):
    match method:
        case "GRPC":
            return grpcClient()
        
        case "HTTP":
            return httpClient()

        case "other":
            pass
    
        

    
    