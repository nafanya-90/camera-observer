from abc import abstractmethod
from app.api.queues.abstract_queue import AbstractQueue

class AbstractQueueProducer(AbstractQueue):
    """
     Sends messages to a queue server
    """

    @abstractmethod
    def publish(self, message: str):
        raise NotImplementedError("Subclasses should implement this!")
