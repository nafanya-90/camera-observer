import logging
import pika

from queues.abstract_queue import AbstractQueue


class RabbitMQ(AbstractQueue):
    """
     Connect to a RabbitMQ server
    """

    def __init__(self, queue, host, routing_key, username, password,
                 exchange=''):
        self._queue = queue
        self._host = host
        self._routing_key = routing_key
        self._exchange = exchange
        self._username = username
        self._password = password

        self._connection = None
        self._channel = None

    def start_connection(self):
        """
         Connect to the queue server, create a channel, an exchange and a bind
        """
        if self._connection and self._connection.is_open:
            return

        self._create_channel()
        self._create_exchange()
        self._create_bind()
        logging.info("Connection created")

    def close_connection(self):
        """
         Close connection to the queue server
        """
        if not self._connection or self._connection.is_closed:
            return

        self._connection.close()
        logging.info("Connection closed")

    def _create_channel(self):
        credentials = pika.PlainCredentials(username=self._username,
                                            password=self._password)
        parameters = pika.ConnectionParameters(self._host,
                                               credentials=credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def _create_exchange(self):
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='fanout',
            passive=False,
            durable=True,
            auto_delete=False
        )
        self._channel.queue_declare(queue=self._queue, durable=False)

    def _create_bind(self):
        self._channel.queue_bind(
            queue=self._queue,
            exchange=self._exchange,
            routing_key=self._routing_key
        )
