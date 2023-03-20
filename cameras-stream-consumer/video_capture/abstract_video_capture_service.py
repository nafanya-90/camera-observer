from abc import ABC, abstractmethod
from observers.abstract_observer import AbstractSubjectObserver

class AbstractVideoCaptureService(AbstractSubjectObserver, ABC):
    """Abstract video capturing service"""

    @property
    def video_url(self):
        """Get video stream url"""
        raise NotImplementedError("Subclasses should implement this!")

    @video_url.setter
    @abstractmethod
    def video_url(self, url):
        """Set video stream url"""
        raise NotImplementedError("Subclasses should implement this!")

    @property
    def output_path(self):
        """Get output path to save a video from the stream"""
        raise NotImplementedError("Subclasses should implement this!")

    @output_path.setter
    @abstractmethod
    def output_path(self, output):
        """Set output path to save a video from the stream"""
        raise NotImplementedError("Subclasses should implement this!")

    @abstractmethod
    def start(self, break_in_sec: int = None):
        """Start the capturing process"""
        raise NotImplementedError("Subclasses should implement this!")

    @abstractmethod
    def stop(self):
        """Stop the capturing process"""
        raise NotImplementedError("Subclasses should implement this!")