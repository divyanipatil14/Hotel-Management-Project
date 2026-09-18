from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

from models.room import Room

app = FastAPI(title="Hotel Management System")

FILE_PATH = "data/room.json"

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