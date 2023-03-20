from abc import ABC, abstractmethod


class AbstractSubjectObserver(ABC):
    """
        The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: 'AbstractObserver') -> None:
        """
            Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: 'AbstractObserver') -> None:
        """
            Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
            Notify all observers about an event.
        """
        pass


class AbstractObserver(ABC):
    """
        The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: AbstractSubjectObserver) -> None:
        """
            Receive update from subject.
        """
        pass