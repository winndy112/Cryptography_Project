# import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models import Base, Students, Ins, Quals
from passlib.context import CryptContext # for hash password
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from fastapi.responses import JSONResponse
import base64
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta, datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]    
router = APIRouter()

class GetQualsRequest(BaseModel):
    student_id: int
    school: str
    first_name: str
    last_name: str
    qual_code: int

@router.get("/",  status_code=status.HTTP_200_OK)

@router.post("/get_quals")
async def get_qualifications(data: dict, db: Session = Depends(get_db)):
    # Extract input parameters from the request data
    student_id = data.get("student_id")
    school = data.get("school")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    qual_code = data.get("qual_code")

    student_info = db.query(Students).filter(
        Students.id_sv == student_id,
        Students.school == school,
        Students.first_name == first_name,
        Students.last_name == last_name
    ).first()
    # check student if exist
    if not student_info:
        raise HTTPException(status_code=404, detail="Student not found")

    qual_info = db.query(Quals).filter(
        Quals.id_sv == student_info.id_sv,
        Quals.degree_code == qual_code
    ).first()

    # Check qualification if exist
    if not qual_info:
        raise HTTPException(status_code=404, detail="Qualification not found")
    pdf_file_content = qual_info.pdf_file
    # Assume that the result is a file content (PDF file in this case)
    pdf_base64 = base64.b64encode(pdf_file_content).decode("utf-8")
    # trả về frontend nội dung file pdf đã được encode base64
    
    response_data = {
        "pdf_content_base64": pdf_base64,
    }
    return JSONResponse(content=response_data)