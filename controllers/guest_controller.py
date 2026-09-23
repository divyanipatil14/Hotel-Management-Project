from fastapi import APIRouter
from services.guest_service import GuestService
from models.guest_schema import GuestCreateRequest
from models.guest_schema import GuestUpdateRequest
router = APIRouter(prefix="/api/guests", tags=["Guests"])
guest_service = GuestService()

@router.get("")
def get_guests():
    # print("Get all Guest..........")
    return guest_service.get_all_guests()

@router.post("")
def add_guest(guest_data: GuestCreateRequest):
    # print(f"guests request................. {guest_data}")
    created_guest = guest_service.add_guest(guest_data)
    return {"message": "Guest checked in successfully", "guest": created_guest}

@router.put("/{guest_id}")
def update_guest(guest_id: int, update_data: GuestUpdateRequest):
    # print(f"update request........ {update_data}")
    return guest_service.update_guest(guest_id, update_data)

@router.post("/{guest_id}/checkout")
def checkout_guest(guest_id: int):
    # print(f"checkout request..........")
    return guest_service.checkout_guest(guest_id)