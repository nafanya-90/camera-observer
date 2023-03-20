from abc import abstractmethod
from queues.abstract_queue import AbstractQueue

class AbstractQueueConsumer(AbstractQueue):
    """
     Consumes messages from a queue server
    """

    @abstractmethod
    def get_messages(self):
        pass
