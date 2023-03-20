from abc import ABC, abstractmethod

class AbstractQueue(ABC):

    @abstractmethod
    def start_connection(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass
