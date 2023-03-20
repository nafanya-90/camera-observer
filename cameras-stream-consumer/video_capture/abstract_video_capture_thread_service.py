from abc import abstractmethod
from video_capture.abstract_video_capture_service import AbstractVideoCaptureService

class AbstractVideoCaptureThreadService(AbstractVideoCaptureService):

    @property
    def event(self):
        """Get thread event to manage the thread inside a callback"""
        raise NotImplementedError("Subclasses should implement this!")

    @event.setter
    @abstractmethod
    def event(self, url):
        """Set thread event to manage the thread inside a callback"""
        raise NotImplementedError("Subclasses should implement this!")