from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from controllers.room_controller import router as room_router

app = FastAPI(title="Hotel Management System")

# Router connect karna
app.include_router(room_router)

# Frontend static files & Home route
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")