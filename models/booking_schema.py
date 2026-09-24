from pydantic import BaseModel

class BookingCreateRequest(BaseModel):
    booking_id: int
    guest_id: int
    room_id: int
    check_in_date: str    
    check_out_date: str  