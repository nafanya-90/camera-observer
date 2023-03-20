import logging
from observers.abstract_observer import AbstractObserver, AbstractSubjectObserver
from queues.abstract_queue_producer import AbstractQueueProducer


class VideoObserver(AbstractObserver):
    def __init__(self, queue_producer: AbstractQueueProducer):
        self._queue_producer = queue_producer

    def update(self, subject: AbstractSubjectObserver) -> None:
        """
            Add a new message to the queue when a new video from a camera is saved.
            The message should be consumed by another service to upload the file
            somewhere in the cloud
        """
        self._queue_producer.start_connection()
        logging.debug(f"Saved video filename: {subject._last_saved_filepath}")
        self._queue_producer.publish(message={
            "video_filepath": subject._last_saved_filepath}
        )
