from abc import ABC, abstractmethod

class AbstractQueue(ABC):
    """
     Connect to a queue server
    """

    @abstractmethod
    def start_connection(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass
