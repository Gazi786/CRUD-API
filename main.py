from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.student_routes import router as student_router
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

app = FastAPI(title="College Management System API")

# -----------------------------
# 1. Upload folder setup
# -----------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------
# 2. Photo Base URL (local fallback)
# -----------------------------
PHOTO_BASE_URL = os.getenv("PHOTO_BASE_URL", "http://127.0.0.1:8000/uploads")
app.state.PHOTO_BASE_URL = PHOTO_BASE_URL

# -----------------------------
# 3. Serve uploads folder (ONLY ONE)
# -----------------------------
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# -----------------------------
# 4. Include API routes
# -----------------------------
app.include_router(student_router, prefix="/api")

# -----------------------------
# 5. Welcome route
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to College Management System API",
        "photo_base_url": app.state.PHOTO_BASE_URL
    }



































# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from routes.student_routes import router as student_router
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load .env file

# app = FastAPI(title="College Management System API")

# # Uploads folder
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # Read photo base URL from .env (fallback for local)
# PHOTO_BASE_URL = os.getenv("PHOTO_BASE_URL", "http://127.0.0.1:8000/uploads")
# app.state.PHOTO_BASE_URL = PHOTO_BASE_URL

# # Serve uploads folder (ONLY ONE TIME)
# app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# # Include Routers
# app.include_router(student_router, prefix="/api")

# @app.get("/")
# def home():
#     return {
#         "message": "Welcome to College Management System API",
#         "photo_base_url": app.state.PHOTO_BASE_URL
#     }
