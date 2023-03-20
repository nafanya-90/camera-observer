from abc import ABC, abstractmethod
from threading import Event
from video_capture.abstract_video_capture_thread_service import AbstractVideoCaptureThreadService


class AbstractVideoCaptureFactory(ABC):
    """An abstract factory to create different video capture services"""

    @abstractmethod
    def create_video_capture_thread_service(self, video_url: str, output: str,
                                            event: Event) -> AbstractVideoCaptureThreadService:
        pass
