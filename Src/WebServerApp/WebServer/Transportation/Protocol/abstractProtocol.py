from abc import ABC, abstractmethod

class abstractProtocol(ABC):
    @abstractmethod
    def request(self, data):
        pass

    @abstractmethod
    def close(self):
        pass
