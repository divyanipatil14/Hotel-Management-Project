from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from controllers.room_controller import router as room_router
from controllers.guest_controller import router as guest_router
from controllers.booking_controller import router as booking_router
app = FastAPI(title="Hotel Management System")

app.include_router(room_router)
app.include_router(guest_router)
app.include_router(booking_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")