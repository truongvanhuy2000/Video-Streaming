from abc import ABC, abstractmethod

class clientProtocol(ABC):
    @abstractmethod
    def request(self, video, model):
        pass

    @abstractmethod
    def response(self):
        pass