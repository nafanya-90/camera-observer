import os
import logging

from queues.rabbitmq_queue.rabbitmq_consumer import RabbitMQConsumer
from upload.upload_service import AWSUploadService


def main():
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO
    )

    upload_service = AWSUploadService()

    # Get messages from 'video upload' queue
    server = RabbitMQConsumer(
        upload_service=upload_service,
        queue=os.getenv('RABBITMQ_QUEUE'),
        host=os.getenv('RABBITMQ_HOST'),
        routing_key=os.getenv('RABBITMQ_ROUTING_KEY'),
        username=os.getenv('RABBITMQ_USERNAME'),
        password=os.getenv('RABBITMQ_PASSSWORD'),
        exchange=os.getenv('RABBITMQ_EXCHANGE')
    )
    server.start_connection()
    server.get_messages()


if __name__ == "__main__":
    main()