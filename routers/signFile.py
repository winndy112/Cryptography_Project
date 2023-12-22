# import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile
from pydantic import BaseModel
from passlib.context import CryptContext # for hash password
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import logging
from jose import jwt, JWTError
from datetime import timedelta, datetime, date
from fastapi.responses import JSONResponse, FileResponse
import json
import hashlib
import pickle
import base64
import os 
import re
import qr
from models import Students, Ins, Quals
import digital_signature as dsa
import certificate

router = APIRouter()

logging.basicConfig(level=logging.DEBUG) # log dùng để debug
SECRET_KEY = '5d3711a26b488b38642c948a7bc8fa09fe9ba78a2d6b57cac46a34bb0f840147' # key from unique user
ALGORITHM = "HS256" # algorithm

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # instace to hashing password
'''
Form data request khi user muốn kí văn bằng
'''
class SignFileRequest(BaseModel):
    school: str
    firstName: str
    lastName: str
    inputFile: str #base64 encode
    privateKey: str #base64 encode

'''
Lấy session kết nối database
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)] 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Ins).filter(Ins.email_address == email).first()
    if user is None:
        raise credentials_exception
    return user

def is_user_logged_in(request: Request, current_user: Ins = Depends(get_current_user)):
    return current_user is not None

    
@router.post("/sign_file")
async def sign_file(request: Request, db: db_dependency, form_data: SignFileRequest):    # Ensure the files are saved to the server
    try:
        pdf_tmp =  "test/tmp.pdf"
        image_tmp = "image/qrcode.png"
        if not is_user_logged_in(request): 
            raise HTTPException(status_code=401, detail="User not logged in")
            
        _school = form_data.school
        _first_name = form_data.firstName
        _last_name = form_data.lastName
        input_file = form_data.inputFile #base64
        private_key = form_data.privateKey # base64
        # check xem student đã có trong database chưa
        student = db.query(Students).filter(Students.school == _school,
                                            Students.first_name == _first_name, Students.last_name == _last_name ).first()
        
        if not student:
            # If the student is not in the database, add them
            new_student = Students(school=_school, first_name=_first_name, last_name= _last_name )
            db.add(new_student)
            db.commit()
            db.refresh(new_student)
            student_id = new_student.id_sv
        else:
            # If the student is in the database, retrieve their ID
            student_id = student.id_sv
        
        pair = dsa.digital_signature()
        private_key = base64.b64decode(private_key)
        pair.load_private_key(private_key)

        # kí file
        input_bytes = base64.b64decode(input_file)
        pair.signing_pdf(input_bytes)
        # lấy file cert của nhà phát hành từ database
        current_user = get_current_user(request.headers["Authorization"].split()[1], db)

        certificate_file = current_user.certificate_file # base64 encode và đọc vào bytes
        
        # thêm certificate và signature vào file metadata của pdf
        pair.add_data_to_metadata(input_bytes, certificate_file, pdf_tmp)
        with open(pdf_tmp, "rb") as file:
            byte = file.read()
        # thêm qr code vào pdf
        pdf_output:bytes = qr.generateQr_and_add_to_pdf(pair.signature, byte, image_tmp)
        # lưu vào database
        qualification = Quals(
            id_sv=student_id,
            issue_date=date.today(),
            expiration_date=date.today() + timedelta(days=365),  # văn bằng có hiêu lực 1 năm
            institution_id=current_user.institution_id,
            pdf_file=pdf_output,
        )
        db.add(qualification)
        db.commit()

        # dữ liệu trả về
        pdf_output_base64 = base64.b64encode(pdf_output).decode('utf-8')
        response_json = {
            "pdf_content": pdf_output_base64,
            "nhaPhatHanh": current_user.institution_name,
            "nguoiKi" : current_user.authority_person,
            "id_sv" : student_id
        }
        
        os.remove(pdf_tmp)
        os.remove(image_tmp)
        # Return the response
        return JSONResponse(content=response_json)
    except Exception as e:
        logging.exception("An error occurred during file signing:")
        raise HTTPException(status_code=500, detail="Internal Server Error")