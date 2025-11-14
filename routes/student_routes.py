from fastapi import APIRouter, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse
from db.database import get_connection
from models.student import Student
from dotenv import load_dotenv
import shutil
import os

router = APIRouter()

router = APIRouter()

# Load environment variables
load_dotenv()

# Upload directory (Render safe)
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "static/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Base URL for photos
PHOTO_BASE_URL = os.getenv("PHOTO_BASE_URL")


# ==========================================================
#  Route to serve uploaded images
# ==========================================================
@router.get("/uploads/{filename}")
def get_uploaded_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)




# ==========================================================
# 1. Add Student
# ==========================================================
@router.post("/students")
def add_student(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    gender: str = Form(None),
    phone_number: str = Form(None),
    address: str = Form(None),
    photo: UploadFile = None
):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    photo_filename = None
    photo_url = None

    try:
        cursor = conn.cursor()

        query = """INSERT INTO student(first_name, last_name, email, gender, phone_number, address)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (first_name, last_name, email, gender, phone_number, address))
        conn.commit()

        student_id = cursor.lastrowid

        # Save photo if uploaded
        if photo:
            photo_filename = f"{student_id}_{photo.filename}"
            photo_path = os.path.join(UPLOAD_DIR, photo_filename)

            with open(photo_path, "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)

            photo_url = f"{PHOTO_BASE_URL}/{photo_filename}"

            update_query = "UPDATE student SET photo = %s WHERE student_id = %s"
            cursor.execute(update_query, (photo_filename, student_id))
            conn.commit()

        return {
            "Message": "Student Added Successfully",
            "id": student_id,
            "photo_filename": photo_filename,
            "photo_url": photo_url
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding student: {str(e)}")

    finally:
        cursor.close()
        conn.close()





# ==========================================================
# 2. View Single Student
# ==========================================================
@router.get("/students/{student_id}")
def view_single_student(student_id: int):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()
        query = """
            SELECT student_id, first_name, last_name, date_of_birth, gender,
                   email, phone_number, address, enrollment_date, photo
            FROM student WHERE student_id = %s
        """
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Add full photo URL
        student["photo_url"] = (
            f"{PHOTO_BASE_URL}/{student['photo']}"
            if student.get("photo")
            else None
        )

        return student

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching student: {str(e)}")

    finally:
        cursor.close()
        conn.close()




# ==========================================================
# 3. View All Students
# ==========================================================
@router.get("/students")
def view_all_students():
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id, first_name, last_name, date_of_birth, gender,
                   email, phone_number, address, enrollment_date, photo
            FROM student ORDER BY student_id ASC
        """)
        students = cursor.fetchall()

        for student in students:
            student["photo_url"] = (
                f"{PHOTO_BASE_URL}/{student['photo']}"
                if student.get("photo")
                else None
            )

        return students

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")

    finally:
        cursor.close()
        conn.close()



        

# ==========================================================
# 4. Update Student
# ==========================================================
@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    first_name: str = Form(None),
    last_name: str = Form(None),
    date_of_birth: str = Form(None),
    gender: str = Form(None),
    email: str = Form(None),
    phone_number: str = Form(None),
    address: str = Form(None),
    enrollment_date: str = Form(None),
    photo: UploadFile = None
):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT photo FROM student WHERE student_id = %s", (student_id,))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Student not found")

        current_photo = existing["photo"]
        photo_filename = current_photo

        if photo:
            # Delete old photo
            if current_photo:
                old_path = os.path.join(UPLOAD_DIR, current_photo)
                if os.path.exists(old_path):
                    os.remove(old_path)

            # Save new photo
            photo_filename = f"{student_id}_{photo.filename}"
            photo_path = os.path.join(UPLOAD_DIR, photo_filename)

            with open(photo_path, "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)

        # Build dynamic update
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "email": email,
            "phone_number": phone_number,
            "address": address,
            "enrollment_date": enrollment_date,
            "photo": photo_filename
        }

        update_data = {k: v for k, v in data.items() if v is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        fields = [f"{key} = %s" for key in update_data.keys()]
        values = list(update_data.values()) + [student_id]

        query = f"UPDATE student SET {', '.join(fields)} WHERE student_id = %s"
        cursor.execute(query, tuple(values))
        conn.commit()

        photo_url = (
            f"{PHOTO_BASE_URL}/{photo_filename}" if photo_filename else None
        )

        return {
            "message": "Student updated successfully",
            "id": student_id,
            "updated_fields": list(update_data.keys()),
            "photo": photo_filename,
            "photo_url": photo_url
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")

    finally:
        cursor.close()
        conn.close()



# ==========================================================
# 5. Delete Student
# ==========================================================
@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT photo FROM student WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Student not found")

        photo_name = result["photo"]

        cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
        conn.commit()

        # delete photo
        if photo_name:
            file_path = os.path.join(UPLOAD_DIR, photo_name)
            if os.path.exists(file_path):
                os.remove(file_path)

        return {"message": "Student deleted successfully", "id": student_id}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()