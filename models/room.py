class Room:
    def __init__(self, room_id: int, room_type: str, price: float):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.status = "Available"

    def mark_occupied(self):
        self.status = "Occupied"

    def mark_available(self):
        self.status = "Available"

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "room_type": self.room_type,
            "price": self.price,
            "status": self.status
        }

# if __name__ == "__main__":
#     test_room = Room(101, "Deluxe", 2500)
#     print("Room create:", test_room.to_dict())
#     test_room.mark_occupied()
#     print("chnge the status:", test_room.to_dict())