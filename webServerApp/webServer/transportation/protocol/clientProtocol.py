from abc import ABC, abstractmethod

class clientProtocol(ABC):
    @abstractmethod
    def request(self, video, model, addr, sock):
        pass

    @abstractmethod
    def response(self):
        pass