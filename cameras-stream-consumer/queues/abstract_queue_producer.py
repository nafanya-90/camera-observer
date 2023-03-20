from abc import abstractmethod
from queues.abstract_queue import AbstractQueue

class AbstractQueueProducer(AbstractQueue):
    """
     Sends messages to a queue server
    """

    @abstractmethod
    def publish(self, message):
        raise NotImplementedError("Subclasses should implement this!")
