from threading import Event
from video_capture.abstract_video_capture_thread_service import AbstractVideoCaptureThreadService
from video_capture.video_capture_cv2_service import VideoCaptureCV2Service
from video_capture.abstract_video_capture_factory import AbstractVideoCaptureFactory


class VideoCaptureFactory(AbstractVideoCaptureFactory):
    """A factory to create different video capture services"""

    def create_video_capture_thread_service(self, video_url: str, output: str,
                                            event: Event) -> AbstractVideoCaptureThreadService:
        return VideoCaptureCV2Service(video_url, output, event)
