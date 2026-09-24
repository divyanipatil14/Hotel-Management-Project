class Booking:
    def __init__(self, booking_id: int, guest_id: int, room_id: int, check_in_date: str, check_out_date: str, total_days: int, total_amount: float):
        self.booking_id = booking_id
        self.guest_id = guest_id
        self.room_id = room_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_days = total_days
        self.total_amount = total_amount
        self.status = "Confirmed"

    def cancel_booking(self):
        self.status = "Cancelled"

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "guest_id": self.guest_id,
            "room_id": self.room_id,
            "check_in_date": self.check_in_date,
            "check_out_date": self.check_out_date,
            "total_days": self.total_days,
            "total_amount": self.total_amount,
            "status": self.status
        }