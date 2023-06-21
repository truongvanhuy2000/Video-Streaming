from abc import ABC, abstractmethod

class aimodel(ABC):
    @abstractmethod
    def detect(self, frame):
        pass
