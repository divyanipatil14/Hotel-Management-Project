from fastapi import HTTPException
from repositories.room_repository import RoomRepository
from models.room import Room
from models.room_schema import RoomCreateRequest

class RoomService:
    def __init__(self):
        self.repo = RoomRepository()

    def get_all_rooms(self):
        data = self.repo.get_all()
        room_objects = []
        for item in data:
            r = Room(item["room_id"], item["room_type"], item["price"])
            r.status = item["status"]
            room_objects.append(r.to_dict())
        return room_objects

    def add_room(self, room_data: RoomCreateRequest):
        data = self.repo.get_all()

        for item in data:
            if item["room_id"] == room_data.room_id:
                raise HTTPException(status_code=400, detail=f"Room {room_data.room_id} already exists!")

        new_room = Room(room_data.room_id, room_data.room_type, room_data.price)
        data.append(new_room.to_dict())

        self.repo.save_all(data)
        return new_room.to_dict()

    def toggle_room_status(self, room_id: int):
        data = self.repo.get_all()
        room_found = False

        for item in data:
            if item["room_id"] == room_id:
                r = Room(item["room_id"], item["room_type"], item["price"])
                r.status = item["status"]

                if r.status == "Available":
                    r.mark_occupied()
                else:
                    r.mark_available()

                item["status"] = r.status
                room_found = True
                break

        if not room_found:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found!")

        self.repo.save_all(data)
        return {"message": f"Room {room_id} status updated successfully"}