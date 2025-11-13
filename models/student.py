from pydantic import BaseModel
from typing import Optional
from datetime import date

class Student(BaseModel):
    student_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None
