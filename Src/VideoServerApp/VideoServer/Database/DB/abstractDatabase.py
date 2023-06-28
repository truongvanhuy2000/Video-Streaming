from abc import ABC, abstractmethod

class abstractDatabase(ABC):
    @abstractmethod
    def getData(self, key) -> str:
        pass
    @abstractmethod
    def setData(self, key, value):
        pass
    @abstractmethod
    def isExist(self, key) -> bool:
        pass
    