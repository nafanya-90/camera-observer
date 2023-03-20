import logging
import json

from queues.abstract_queue_consumer import AbstractQueueConsumer
from queues.rabbitmq_queue.rabbitmq import RabbitMQ

from stream_service import StreamService


class RabbitMQConsumer(RabbitMQ, AbstractQueueConsumer):
    """
     Consumes messages from a RabbitMQ server
    """

    def __init__(self, stream_service: StreamService, queue: str, host: str,
                 routing_key: str, username: str, password: str, exchange=''):
        super().__init__(queue, host, routing_key, username, password,
                 exchange)
        self._stream_service = stream_service

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
        message = json.loads(body.decode())
        logging.info(f'Consumed message {message["camera"]} from queue')

        camera = message["camera"]
        if camera["is_active"]:
            self._stream_service.connect(camera)
            return

        self._stream_service.disconnect(camera)
