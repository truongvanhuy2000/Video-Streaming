import os
from webServer.transportation.protocol.grpcClient import grpcClient
from webServer.transportation.protocol.httpClient import httpClient

def getTransportMethod(method, address):
    match method:
        case "GRPC":
            return grpcClient(address)
        
        case "HTTP":
            return httpClient(address)

        case "other":
            pass
    
        

    
    