from fastapi import APIRouter
from services.room_service import RoomService
from models.room_schema import RoomCreateRequest, RoomUpdateRequest

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])
room_service = RoomService()

@router.get("")
def get_rooms():
    return room_service.get_all_rooms()

@router.post("")
def add_room(room_data: RoomCreateRequest):
    created_room = room_service.add_room(room_data)
    return {"message": "Room added successfully", "room": created_room}

@router.post("/{room_id}/toggle-status")
def toggle_status(room_id: int):
    return room_service.toggle_room_status(room_id)

@router.put("/{room_id}")
def update_room(room_id: int, update_data: RoomUpdateRequest):
    return room_service.update_room(room_id, update_data)

@router.delete("/{room_id}")
def delete_room(room_id: int):
    return room_service.delete_room(room_id)