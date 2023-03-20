import json
import logging

import pika

from queues.abstract_queue_producer import AbstractQueueProducer
from queues.rabbitmq_queue.rabbitmq import RabbitMQ


class RabbitMQProducer(RabbitMQ, AbstractQueueProducer):
    """
     Sends messages to a RabbitMQ server
    """

    def publish(self, message):
        """
        :param message: message to be published in JSON format
        """

        try:
            self._publish(message)
        except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelWrongStateError):
            logging.debug('reconnecting to queue')
            self.start_connection()
            self._publish(message)

    def _publish(self, message):
        """
        :param message: message to be published in JSON format
        """

        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(content_type='application/json')
        )
        logging.info("Published Message: {}".format(message))