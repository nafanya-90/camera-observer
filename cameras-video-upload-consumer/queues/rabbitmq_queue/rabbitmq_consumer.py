import logging
import json

from queues.abstract_queue_consumer import AbstractQueueConsumer
from queues.rabbitmq_queue.rabbitmq import RabbitMQ

from upload.abstract_upload_service import AbstractUploadService


class RabbitMQConsumer(RabbitMQ, AbstractQueueConsumer):
    """
     Consumes messages from a RabbitMQ server
    """
    def __init__(self, upload_service: AbstractUploadService, queue: str, host: str,
                 routing_key: str, username: str, password: str, exchange=''):
        super().__init__(queue, host, routing_key, username, password,
                 exchange)
        self._upload_service = upload_service

    def get_messages(self, callback=None):
        """Get messages from a queue"""
        if not callback:
            callback = self._callback
        try:
            logging.debug("Starting the server...")
            self._channel.basic_consume(
                queue=self._queue,
                on_message_callback=callback,
                auto_ack=True
            )
            self._channel.start_consuming()
            logging.debug("The server started")
        except Exception as e:
            logging.debug(f'Exception: {e}')

    def _callback(self, channel, method, properties, body):
        try:
            message = json.loads(body.decode())
            logging.info(f'Consumed message {message} from queue')
            self._upload_service.upload(message['video_filepath'])
        except Exception as e:
            logging.error(f'Exception: {e}')
