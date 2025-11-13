from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.student_routes import router as student_router

app = FastAPI(title="College Management System API")

# ✅ Serve uploaded student photos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Include student routes (no .routes)
app.include_router(student_router, prefix="/api")

@app.get("/student")
def home():
    return {"message": "Welcome to College Management System API"}
