from pydantic import BaseModel

class RoomCreateRequest(BaseModel):
    room_id: int
    room_type: str
    price: float