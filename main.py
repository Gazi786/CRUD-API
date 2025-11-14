from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from routes.student_routes import router as student_router
import os

load_dotenv()

app = FastAPI(title="College Management System API")

# Upload folder (same for local + render)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------ SMART AUTO-DETECTION -------------
# If running on Render → use render URL
# If running locally → use localhost automatically
if os.getenv("RENDER"):
    PHOTO_BASE_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/uploads"
else:
    PHOTO_BASE_URL = "http://127.0.0.1:8000/uploads"

app.state.PHOTO_BASE_URL = PHOTO_BASE_URL
# -------------------------------------------------

# Serve uploads folder only once
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routes
app.include_router(student_router, prefix="/api")

@app.get("/")
def home():
    return {
        "message": "Welcome to CMS API",
        "photo_base_url": app.state.PHOTO_BASE_URL
    }
