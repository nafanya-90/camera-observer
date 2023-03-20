from pydantic import BaseModel
from typing import Optional

class CameraIn(BaseModel):
    is_active: bool
    name: str
    location: str
    location_details: Optional[str] = None


class CameraOut(CameraIn):
    id: int


class CameraUpdate(CameraIn):
    is_active: Optional[bool] = None
    name: Optional[str] = None
    location: Optional[str] = None
    location_details: Optional[str] = None
