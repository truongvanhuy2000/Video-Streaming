from abc import ABC, abstractmethod

class protocolServer(ABC):
    @abstractmethod
    def serve(self):
        pass