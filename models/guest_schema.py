from pydantic import BaseModel
from typing import Optional


class GuestCreateRequest(BaseModel):
    guest_id: int
    name: str
    phone: str
    assigned_room_id: int

class GuestUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None