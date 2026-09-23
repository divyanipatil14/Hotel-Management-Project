class Guest:
    def __init__(self, guest_id:int,name:str,phone:str,assigned_room_id:int):
        self.name = name
        self.guest_id =guest_id
        self.phone = phone
        self.assigned_room_id=assigned_room_id
        self.status='checked-In'

    def mark_checked_out(self):
          self.status = "Checked-Out"

    def to_dict(self):
                  return {
                      "guest_id": self.guest_id,
                      "name": self.name,
                      "phone": self.phone,
                      "assigned_room_id": self.assigned_room_id,
                      "status": self.status
                  }
  












