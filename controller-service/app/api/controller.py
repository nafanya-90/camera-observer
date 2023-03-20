from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.models import CameraStateIn, CameraOut
from app.api.service import get_cameras, update_camera_state

controller = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@controller.get('/')
async def home(request: Request):
    cameras = get_cameras()
    return templates.TemplateResponse("index.html",
                                      {"request": request, "cameras": cameras})


@controller.get('/healthcheck', response_model=None)
async def healthcheck():
    return Response(content="UP")


@controller.post('/camera/{id}/update_state', response_model=CameraOut)
async def update_camera(id: int, payload: CameraStateIn):
    camera = update_camera_state(id, payload)
    return camera
