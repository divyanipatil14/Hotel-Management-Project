from pydantic import BaseModel
from typing import Optional

class RoomCreateRequest(BaseModel):
    room_id: int
    room_type: str
    price: float

class RoomUpdateRequest(BaseModel):
    room_type: Optional[str] = None
    price: Optional[float] = None