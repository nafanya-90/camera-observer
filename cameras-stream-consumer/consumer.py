import os
import logging

from queues.rabbitmq_queue.rabbitmq_consumer import RabbitMQConsumer
from queues.rabbitmq_queue.rabbitmq_producer import RabbitMQProducer
from stream_service import StreamService
from video_capture.video_capture_factory import VideoCaptureFactory
from observers.video_observer import VideoObserver


def main():
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO
    )

    # Send messages to 'video upload' queue
    video_queue_producer = RabbitMQProducer(
        queue=os.getenv('RABBITMQ_VIDEO_PRODUCER_QUEUE'),
        host=os.getenv('RABBITMQ_HOST'),
        routing_key=os.getenv('RABBITMQ_VIDEO_PRODUCER_ROUTING_KEY'),
        username=os.getenv('RABBITMQ_USERNAME'),
        password=os.getenv('RABBITMQ_PASSSWORD'),
        exchange=os.getenv('RABBITMQ_VIDEO_PRODUCER_EXCHANGE')
    )

    video_observer = VideoObserver(video_queue_producer)
    video_capture_factory = VideoCaptureFactory()
    stream_service = StreamService(video_capture_factory, video_observer)

    # Get messages from 'camera start/stop capturing' queue
    stream_consumer = RabbitMQConsumer(
        stream_service=stream_service,
        queue=os.getenv('RABBITMQ_QUEUE'),
        host=os.getenv('RABBITMQ_HOST'),
        routing_key=os.getenv('RABBITMQ_ROUTING_KEY'),
        username=os.getenv('RABBITMQ_USERNAME'),
        password=os.getenv('RABBITMQ_PASSSWORD'),
        exchange=os.getenv('RABBITMQ_EXCHANGE')
    )
    stream_consumer.start_connection()
    stream_consumer.get_messages()


if __name__ == "__main__":
    main()