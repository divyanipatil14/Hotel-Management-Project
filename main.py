from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os

from models.room import Room

app = FastAPI(title="Hotel Management System")

FILE_PATH = "data/room.json"

class RoomCreateRequest(BaseModel):
    room_id: int
    room_type: str
    price: float

def read_rooms():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def write_rooms(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

@app.get("/api/rooms")
def get_rooms():
    data = read_rooms()
    room_objects = []
    for item in data:
        r = Room(item["room_id"], item["room_type"], item["price"])
        r.status = item["status"]
        room_objects.append(r.to_dict())
    return room_objects

@app.post("/api/rooms")
def add_room(room_data: RoomCreateRequest):
    data = read_rooms()

    for item in data:
        if item["room_id"] == room_data.room_id:
            raise HTTPException(status_code=400, detail=f"Room {room_data.room_id} already exists!")

    new_room = Room(room_data.room_id, room_data.room_type, room_data.price)

    data.append(new_room.to_dict())

    write_rooms(data)
    return {"message": "Room added successfully", "room": new_room.to_dict()}

@app.post("/api/rooms/{room_id}/toggle-status")
def toggle_room_status(room_id: int):
    data = read_rooms()
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

    if room_found:
        write_rooms(data)
        return {"message": f"Room {room_id} status updated successfully"}
    return {"error": "Room not found"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")