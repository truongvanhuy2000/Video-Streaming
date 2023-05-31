from webServer.transportation.protocol.clientProtocol import clientProtocol

class httpClient(clientProtocol):
    def __init__(self) -> None:
        super().__init__()

    def request(self, video, model, addr):
        pass

    def response(self):
        pass