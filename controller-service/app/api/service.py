"""The module to manage RESTApi access to the camera service"""

import os
import httpx

from fastapi import HTTPException

from app.api.models import CameraStateIn

CAMERAS_SERVICE_HOST_URL = 'http://cameras_service/api/v1/cameras/'
url = os.environ.get('CAMERAS_SERVICE_HOST_URL') or CAMERAS_SERVICE_HOST_URL


def is_camera_present(camera_id: int):
    """Check if the camera exists"""
    r = httpx.get(f'{url}{camera_id}')
    return True if r.status_code == 200 else False

def get_cameras():
    """Get data for all cameras"""
    r = httpx.get(f'{url}')
    if not r.status_code == 200:
        raise HTTPException(status_code=500, detail=f"Error getting active cameras. "
                                   f"Status code: {r.status_code}")
    return r.json()


def update_camera_state(id: int, payload: CameraStateIn):
    """Update the camera instance"""
    r = httpx.patch(f'{url}{id}', json=payload.dict())
    if not r.status_code == 200:
        raise HTTPException(status_code=500, detail=f"Error updating camera state. "
                                   f"Status code: {r.status_code}")
    return r.json()
