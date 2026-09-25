from fastapi import APIRouter
from services.booking_service import BookingService
from models.booking_schema import BookingCreateRequest
router = APIRouter(prefix="/api/bookings", tags=["Bookings"])
booking_service = BookingService()

@router.get("")
def get_bookings():
    print("bookings request received..........")
    return booking_service.get_all_bookings()

@router.post("")
def create_booking(booking_data: BookingCreateRequest):
    print("bookings request received data..........")
    created_booking = booking_service.create_booking(booking_data)
    return {"message": "Booking confirmed successfully", "booking": created_booking}

@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: int):
    return booking_service.cancel_booking(booking_id)