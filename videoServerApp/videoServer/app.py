from videoServer.transportation import protocolProvider
import os

def run():
    protocolType = os.getenv('TRANSPORT_METHOD')
    # protocolType = "GRPC"
    if protocolType == None:
        print("No env variable for protocol type")
        exit()
    protocolServer = protocolProvider.getProtocol(protocolType)
    protocolServer.serve()