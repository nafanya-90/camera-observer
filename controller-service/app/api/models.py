from pydantic import BaseModel


class CameraOut(BaseModel):
    id: int
    is_active: bool
    name: str
    location: str
    location_details: str


class CameraStateIn(BaseModel):
    is_active: bool
