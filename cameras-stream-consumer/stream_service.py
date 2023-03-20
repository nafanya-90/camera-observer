import logging

from typing import Dict, Hashable, Optional
from dataclasses import dataclass
from threading import Thread, Event
from video_capture.abstract_video_capture_factory import AbstractVideoCaptureFactory
from observers.abstract_observer import AbstractObserver


@dataclass
class ThreadsWithEvent:
    """
        Every instance should contain a thread object and an event object
        associated with the thread
    """
    thread: Thread
    event: Event

    def start(self):
        """Start the thread"""
        self.thread.start()

    def stop(self):
        """Stop the thread"""
        self.event.set()


class StreamService:
    """The service is responsible to manage camera streams using threads"""

    def __init__(self, video_capture_factory: AbstractVideoCaptureFactory,
                 video_observer: AbstractObserver):
        """
            :param video_capture_factory: A factory to create an object that is responsible to capture a stream
            :param video_observer: An observer to notify subscribers about updates in video capture objects
        """
        self._threads = {}
        self._video_capture_factory = video_capture_factory
        self._video_observer = video_observer

    def connect(self, camera: dict):
        """
            Connect to a new camera.
            It creates a new connection and start capturing in separate thread.
        """
        logging.info(f"Connect camera: {camera}")
        event = Event()
        threads_with_event = ThreadsWithEvent(
            event=event,
            thread=Thread(target=StreamService.capture_stream,
                          args=(event, camera, self._video_capture_factory,
                                self._video_observer))
        )
        thread = self._add_thread(camera['id'], threads_with_event)
        thread.start()

    def disconnect(self, camera: dict):
        """
            Disconnect the camera.
            It sends event to the thread to stop capturing and stop the thread.
        """
        thread = self._get_thread(camera['id'])
        if not thread:
            return

        thread.stop()
        del self._threads[camera['id']]

        logging.info(f"Disconnect camera: {camera}")

    def _get_thread(self, key: Hashable) -> Optional[ThreadsWithEvent]:
        if key not in self._threads:
            return None

        return self._threads[key]

    def _add_thread(self, key: Hashable, thread: ThreadsWithEvent) -> ThreadsWithEvent:
        if key in self._threads:
            raise Exception(f"Thread {key} already exists")

        self._threads[key] = thread
        return thread

    @staticmethod
    def capture_stream(event, camera: dict,
                       video_capture_service_factory: AbstractVideoCaptureFactory,
                       video_observer: AbstractObserver):
        """
            A callback method for a camera capturing thread.
            It creates a new video capture service, attach observers and
            run capturing
        """
        logging.info(f"Capture stream from {camera['url']}")
        video_capture_service = video_capture_service_factory.create_video_capture_thread_service(
            video_url=camera['url'],
            output=f'/tmp/output_id_{camera["id"]}.mp4',
            event=event,
        )
        video_capture_service.attach(video_observer)
        video_capture_service.start(10)
