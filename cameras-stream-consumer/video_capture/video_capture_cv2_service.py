import cv2
import logging
import time
import hashlib
import os

from typing import List
from threading import Event
from video_capture.abstract_video_capture_thread_service import AbstractVideoCaptureThreadService
from observers.abstract_observer import AbstractObserver


class VideoCaptureCV2Service(AbstractVideoCaptureThreadService):
    """Capture video from camera service based on open-cv package"""

    def __init__(self, video_url: str = None, output = None,
                 event: Event = None):
        """
            :param video_url: camera url or video stream url
            :param output: output path for saved videos
            :param event: thread event to manage camera capturing callback
        """

        self._output_path_name = None
        self._output_path_ext = None

        self._cap = None
        self._fourcc = None
        self._writer = None
        self._last_saved_filepath = None

        self._is_active_stream = False

        self.video_url = video_url
        self.output_path = output
        self.event = event

        self._observers: List[AbstractObserver] = []

    @property
    def video_url(self):
        """Get video stream url"""
        return self._video_url

    @video_url.setter
    def video_url(self, url):
        """Set video stream url"""
        self._video_url = url

    @property
    def output_path(self):
        """Get output path to save a video from the stream"""
        return self._output_path

    @output_path.setter
    def output_path(self, output):
        """Set output path to save a video from the stream"""
        self._output_path = output
        self._output_path_name, self._output_path_ext = os.path.splitext(output)

    @property
    def output_path_name(self):
        """Get stream videos output path name"""
        return self._output_path_name

    @property
    def output_path_ext(self):
        """Get stream videos output path extension"""
        return self._output_path_ext

    @property
    def event(self):
        """Get stream videos thread event"""
        return self._event

    @event.setter
    def event(self, event: Event):
        """Set stream videos thread event"""
        self._event = event

    def attach(self, observer: AbstractObserver) -> None:
        """
            Attach an observer to the subject.
        """
        logging.info("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: AbstractObserver) -> None:
        """
            Detach an observer from the subject.
        """
        self._observers.remove(observer)

    def notify(self) -> None:
        """
            Notify all observers about an event.
        """
        logging.info("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def start(self, break_in_sec: int = None):
        """Start the capturing process"""

        self._is_active_stream = True
        # initialise capture service based on open-cv
        self._cap = cv2.VideoCapture(self.video_url)

        # Get video metadata
        video_fps = self._cap.get(cv2.CAP_PROP_FPS),
        height = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)

        filepath = self.output_path

        logging.debug(f"Meta data: {video_fps}, {height}, {height}")
        logging.debug(f"Output path: {self.output_path}")

        self._fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        self._writer = cv2.VideoWriter(filepath,
                                 apiPreference=0,
                                 fourcc=self._fourcc,
                                 fps=video_fps[0],
                                 frameSize=(int(width), int(height)))

        start_time_in_seconds = time.time()
        # capture the video frame-by-frame until it brakes
        while True:
            # get a new frame
            ret, frame = self._cap.read()
            if not ret or self.event.is_set():
                self._last_saved_filepath = filepath
                self._destroy()
                self.notify()
                break  # break if it can't receive the frame

            logging.debug(f'Write a frame from {self.video_url}')
            self._writer.write(frame)  # write the frame

            # check based on time if we need to save captured frames to the file
            # and start capturing to a new file
            if break_in_sec and time.time() - start_time_in_seconds >= break_in_sec:
                # add hash string to the default file name to save the stream in
                # different files
                md5_hash = hashlib.md5(str(time.time()).encode()).hexdigest()
                self._last_saved_filepath = filepath
                filepath = f"{self.output_path_name}.{md5_hash}{self.output_path_ext}"
                logging.info(f'Filepath changed')
                logging.debug(f'New filepath is {filepath}')

                # save the stream to the file and start capturing to a new file
                self._writer.release()
                self._writer = cv2.VideoWriter(filepath,
                                               apiPreference=0,
                                               fourcc=self._fourcc,
                                               fps=video_fps[0],
                                               frameSize=(
                                               int(width), int(height)))

                # use observer pattern to let others know that a new video is ready
                self.notify()
                start_time_in_seconds = time.time()

    def stop(self):
        """Stop the capturing process"""
        self._event.set()

    def _destroy(self):
        self._is_active_stream = False
        self._writer.release()
        self._cap.release()
        cv2.destroyAllWindows()
