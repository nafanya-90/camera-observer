from abc import ABC, abstractmethod

class AbstractQueue(ABC):
    """
     Connect to a queue server
    """

    @abstractmethod
    def start_connection(self):
        raise NotImplementedError("Subclasses should implement this!")

    @abstractmethod
    def close_connection(self):
        raise NotImplementedError("Subclasses should implement this!")
