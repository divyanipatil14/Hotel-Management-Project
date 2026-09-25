from fastapi import HTTPException
from datetime import datetime
from repositories.booking_repository import BookingRepository
from repositories.guest_repository import GuestRepository
from repositories.room_repository import RoomRepository
from models.booking import Booking
from models.booking_schema import BookingCreateRequest

class BookingService:
    def __init__(self):
        self.booking_repo = BookingRepository()
        self.guest_repo = GuestRepository()
        self.room_repo = RoomRepository()

    def get_all_bookings(self):
        data = self.booking_repo.get_all()
        booking_list = []
        for item in data:
            b = Booking(
                booking_id=item["booking_id"],
                guest_id=item["guest_id"],
                room_id=item["room_id"],
                check_in_date=item["check_in_date"],
                check_out_date=item["check_out_date"],
                total_days=item["total_days"],
                total_amount=item["total_amount"]
            )
            b.status = item["status"]
            booking_list.append(b.to_dict())
        return booking_list


    def create_booking(self, booking_data: BookingCreateRequest):
        bookings = self.booking_repo.get_all()
        guests = self.guest_repo.get_all()
        rooms = self.room_repo.get_all()

        for b in bookings:
            if b["booking_id"] == booking_data.booking_id:
                raise HTTPException(status_code=400, detail=f"Booking ID {booking_data.booking_id} already exists!")

        target_guest = None
        for g in guests:
            if g["guest_id"] == booking_data.guest_id:
                target_guest = g
                break

        if not target_guest:
            raise HTTPException(status_code=404, detail=f"Guest ID {booking_data.guest_id} does not exist!")

        target_room = None
        for r in rooms:
            if r["room_id"] == booking_data.room_id:
                target_room = r
                break

        if not target_room:
            raise HTTPException(status_code=404, detail=f"Room {booking_data.room_id} does not exist!")

        if target_room["status"] == "Occupied":
            raise HTTPException(status_code=400, detail=f"Room {booking_data.room_id} is already occupied!")

        try:
            d1 = datetime.strptime(booking_data.check_in_date, "%Y-%m-%d")
            d2 = datetime.strptime(booking_data.check_out_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Dates must be in YYYY-MM-DD format!")

        total_days = (d2 - d1).days
        if total_days <= 0:
            raise HTTPException(status_code=400, detail="Check-out date must be at least 1 day after check-in date!")

        total_amount = float(total_days * target_room["price"])

        target_room["status"] = "Occupied"
        self.room_repo.save_all(rooms)

        new_booking = Booking(
            booking_id=booking_data.booking_id,
            guest_id=booking_data.guest_id,
            room_id=booking_data.room_id,
            check_in_date=booking_data.check_in_date,
            check_out_date=booking_data.check_out_date,
            total_days=total_days,
            total_amount=total_amount
        )
        bookings.append(new_booking.to_dict())
        self.booking_repo.save_all(bookings)

        return new_booking.to_dict()

    def cancel_booking(self, booking_id: int):
        bookings = self.booking_repo.get_all()
        rooms = self.room_repo.get_all()

        target_booking = None
        for b in bookings:
            if b["booking_id"] == booking_id:
                target_booking = b
                break

        if not target_booking:
            raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found!")

        if target_booking["status"] == "Cancelled":
            raise HTTPException(status_code=400, detail=f"Booking {booking_id} has already been cancelled!")

        target_booking["status"] = "Cancelled"

        room_id = target_booking["room_id"]
        for r in rooms:
            if r["room_id"] == room_id:
                r["status"] = "Available"
                break

        self.room_repo.save_all(rooms)
        self.booking_repo.save_all(bookings)

        return {"message": f"Booking {booking_id} cancelled successfully. Room {room_id} is now Available."}