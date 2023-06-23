from abc import ABC, abstractmethod

class abstractConsumer(ABC):
    @abstractmethod
    def consume(self, topic):
        pass

    @abstractmethod
    def createTopic(self, **kwargs):
        pass