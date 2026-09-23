from fastapi import HTTPException
from repositories.guest_repository import GuestRepository
from repositories.room_repository import RoomRepository
from models.guest import Guest
from models.guest_schema import GuestCreateRequest, GuestUpdateRequest

class GuestService:
    def __init__(self):
        # print("both repositories.........")
        self.guest_repo = GuestRepository()
        self.room_repo = RoomRepository()

    def get_all_guests(self):
        data = self.guest_repo.get_all()
        
        guest_list = []
        for item in data:
            g = Guest(item["guest_id"], item["name"], item["phone"], item["assigned_room_id"])
            g.status = item["status"]
            guest_list.append(g.to_dict())
            
        print(f"--> [SERVICE] Total {len(guest_list)} guests mile.")
        return guest_list


    def add_guest(self, guest_data: GuestCreateRequest):
        guests = self.guest_repo.get_all()
        rooms = self.room_repo.get_all()

        for g in guests:
            if g["guest_id"] == guest_data.guest_id:
                raise HTTPException(status_code=400, detail=f"Guest ID {guest_data.guest_id} already exists!")

        target_room = None
        for r in rooms:
            if r["room_id"] == guest_data.assigned_room_id:
                target_room = r
                break

        if not target_room:
            raise HTTPException(status_code=404, detail=f"Room {guest_data.assigned_room_id} does not exist!")

        if target_room["status"] == "Occupied":
            raise HTTPException(status_code=400, detail=f"Room {guest_data.assigned_room_id} is already occupied!")

        target_room["status"] = "Occupied"
        self.room_repo.save_all(rooms)

        new_guest = Guest(guest_data.guest_id, guest_data.name, guest_data.phone, guest_data.assigned_room_id)
        guests.append(new_guest.to_dict())
        self.guest_repo.save_all(guests)

        return new_guest.to_dict()

    def update_guest(self, guest_id: int, update_data: GuestUpdateRequest):
        guests = self.guest_repo.get_all()
        target_guest = None

        for g in guests:
            if g["guest_id"] == guest_id:
                target_guest = g
                break

        if not target_guest:
            print(f"[ERROR] Guest ID {guest_id} not found in database!")
            raise HTTPException(status_code=404, detail=f"Guest {guest_id} not found!")

        if update_data.name is not None:
            target_guest["name"] = update_data.name

        if update_data.phone is not None:
            target_guest["phone"] = update_data.phone

        self.guest_repo.save_all(guests)
        return {"message": f"Guest {guest_id} updated successfully", "guest": target_guest}

    def checkout_guest(self, guest_id: int):
        print(f"checkout for Guest ID: {guest_id}...")
        guests = self.guest_repo.get_all()
        rooms = self.room_repo.get_all()

        target_guest = None
        for g in guests:
            if g["guest_id"] == guest_id:
                target_guest = g
                break

        if not target_guest:
            print(f"Guest ID {guest_id} not found!")
            raise HTTPException(status_code=404, detail=f"Guest {guest_id} not found!")

        if target_guest["status"] == "Checked-Out":
            print(f"Guest ID {guest_id} is already checked out.")
            raise HTTPException(status_code=400, detail=f"Guest {guest_id} has already checked out!")

        target_guest["status"] = "Checked-Out"
        print(f"{guest_id} status updated to checked out.")

        assigned_room_id = target_guest["assigned_room_id"]
        for r in rooms:
            if r["room_id"] == assigned_room_id:
                r["status"] = "Available"
                break

        self.room_repo.save_all(rooms)
        self.guest_repo.save_all(guests)
        print("Both json file successfully!")

        return {"message": f"Guest {guest_id} checked out successfully. Room {assigned_room_id} is now Available."}