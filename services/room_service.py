from fastapi import HTTPException
from repositories.room_repository import RoomRepository
from models.room import Room
from models.room_schema import RoomCreateRequest, RoomUpdateRequest

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

    def update_room(self, room_id: int, update_data: RoomUpdateRequest):
        data = self.repo.get_all()
        target_room = None

        for item in data:
            if item["room_id"] == room_id:
                target_room = item
                break

        if not target_room:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found!")

        if update_data.room_type is not None:
            target_room["room_type"] = update_data.room_type
        if update_data.price is not None:
            target_room["price"] = update_data.price

        self.repo.save_all(data)
        return {"message": f"Room {room_id} updated successfully", "room": target_room}

    def delete_room(self, room_id: int):
        data = self.repo.get_all()
        
        room_to_delete = None
        for item in data:
            if item["room_id"] == room_id:
                room_to_delete = item
                break

        if not room_to_delete:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found!")

        if room_to_delete["status"] == "Occupied":
            raise HTTPException(status_code=400, detail="Cannot delete an occupied room! Please check out first.")

        updated_data = [item for item in data if item["room_id"] != room_id]
        self.repo.save_all(updated_data)
        return {"message": f"Room {room_id} deleted successfully"}