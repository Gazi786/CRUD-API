from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.student_routes import router as student_router
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

app = FastAPI(title="College Management System API")


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploads folder
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

PHOTO_BASE_URL = "http://127.0.0.1:8000/uploads"





# Read photo base URL from .env
PHOTO_BASE_URL = os.getenv("PHOTO_BASE_URL")

# Store in app state so routes can access it
app.state.PHOTO_BASE_URL = PHOTO_BASE_URL

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include Routers
app.include_router(student_router, prefix="/api")

@app.get("/")
def home():
    return {
        "message": "Welcome to College Management System API",
        "photo_base_url": app.state.PHOTO_BASE_URL
    }
