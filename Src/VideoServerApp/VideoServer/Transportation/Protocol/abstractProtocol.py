from abc import ABC, abstractmethod

class abstractProtocol(ABC):
    @abstractmethod
    def request(self, route, data):
        pass

    @abstractmethod
    def close(self):
        pass
