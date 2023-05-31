from abc import ABC, abstractmethod

class model(ABC):
    @abstractmethod
    def detect(self, frame):
        pass
