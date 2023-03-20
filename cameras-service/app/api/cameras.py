import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from typing import List

from app.api.models import CameraOut, CameraIn, CameraUpdate
from app.api import db_manager
from app.api.queues.rabbitmq_queue.rabbitmq_producer import RabbitMQProducer

cameras = APIRouter()

# sends messages to the rabbitmq queue
rabbitMQ = RabbitMQProducer(
        queue=os.getenv('RABBITMQ_QUEUE'),
        host=os.getenv('RABBITMQ_HOST'),
        routing_key=os.getenv('RABBITMQ_CAMERA_STATE_UPDATED_ROUTING_KEY'),
        username=os.getenv('RABBITMQ_USERNAME'),
        password=os.getenv('RABBITMQ_PASSSWORD'),
        exchange=os.getenv('RABBITMQ_EXCHANGE')
    )
rabbitMQ.start_connection()


@cameras.get('/healthcheck', response_model=None)
async def healthcheck():
    """Check if the container is alive"""
    return Response(content="UP")


@cameras.get('/', response_model=List[CameraOut])
async def get_cameras():
    """Get data for all available cameras from the DB"""
    return await db_manager.get_all_cameras()


@cameras.patch('/{id}', response_model=CameraOut, status_code=200)
async def update_camera(id: int, payload: CameraUpdate):
    """Update a camera data by the camera ID"""

    camera_before_update = await db_manager.get_camera(id)
    camera = await db_manager.update_camera(id, payload)
    if camera_before_update.is_active != camera.is_active:
        rabbitMQ.publish(message={"camera": dict(camera)})
    return camera


@cameras.post('/', response_model=CameraOut, status_code=201)
async def create_camera(payload: CameraIn):
    """Add a camera to the DB"""
    cast_id = await db_manager.add_camera(payload)

    response = {
        'id': cast_id,
        **payload.dict()
    }

    return response

@cameras.get('/{id}/', response_model=CameraOut)
async def get_camera(id: int):
    """Get a camera data by the camera ID"""
    camera = await db_manager.get_camera(id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera
