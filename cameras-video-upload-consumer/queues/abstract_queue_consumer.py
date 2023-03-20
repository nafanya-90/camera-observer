from abc import abstractmethod
from queues.abstract_queue import AbstractQueue

class AbstractQueueConsumer(AbstractQueue):
    """
     Consumes messages from a RabbitMQ server
    """

    @abstractmethod
    def get_messages(self):
        """Get messages from a queue"""
        pass
