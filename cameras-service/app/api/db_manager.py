from app.api.models import CameraOut, CameraIn, CameraUpdate
from app.api.db import cameras, database


async def get_all_cameras():
    query = cameras.select()
    return await database.fetch_all(query=query)


async def add_camera(payload: CameraIn):
    query = cameras.insert().values(**payload.dict())
    return await database.execute(query=query)


async def update_camera(id: int, payload: CameraIn):
    filtered_payload = {k: v for k, v in payload.dict().items()
                        if v is not None}
    query = (
        cameras
        .update()
        .where(cameras.c.id == id)
        .values(**filtered_payload)
    )
    await database.execute(query=query)
    return await get_camera(id)


async def get_camera(id: int):
    query = cameras.select(cameras.c.id==id)
    return await database.fetch_one(query=query)
