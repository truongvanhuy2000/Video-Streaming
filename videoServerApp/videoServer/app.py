from videoServer.transportation import protocolProvider
import os

def run():
    protocolType = os.getenv('TRANSPORT_METHOD')
    # protocolType = "GRPC"
    protocolServer = protocolProvider.getProtocol(protocolType)
    protocolServer.serve()