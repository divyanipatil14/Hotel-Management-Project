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

@app.get("/api/rooms")
def get_rooms():
    data = read_rooms()
    room_objects = []
    for item in data:
        r = Room(item["room_id"], item["room_type"], item["price"])
        r.status = item["status"]
        room_objects.append(r.to_dict())
        
    return room_objects


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")