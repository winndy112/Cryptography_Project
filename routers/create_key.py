# import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile
from pydantic import BaseModel
from passlib.context import CryptContext # for hash password
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import logging
from jose import jwt, JWTError
from datetime import timedelta, datetime, date
from fastapi.responses import JSONResponse, FileResponse
import json
import hashlib
import pickle
import base64
import os 
import digital_signature as dsa
import certificate

router = APIRouter()

'''
Form data request khi user muốn sign up
'''
class CreateUserRequest(BaseModel):
    institutionName: str
    authority: str
    Email: str
    password: str

'''
Form data request khi user muốn log in
'''
class LoginRequest(BaseModel):
    email: str
    password: str


'''
Lấy session kết nối database
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
# param means: db will be define in a "get_db" function        
db_dependency = Annotated[Session, Depends(get_db)] 

@router.post('/create_key')
async def create_key():
    
    # tạo cặp key cho người dùng
    pair = dsa.digital_signature()
    pair.create_key()
    file = pair.SaveSecret2Pem("./keytmp.pem")
    with open("./keytmp.pem", "rb") as file:
        content = file.read()
    base64_encode = base64.b64encode(content).decode("utf-8")  
    response_data = {
        "Status":"Successfully signed up new institution", 
        "Private_key": base64_encode,
    }
    os.remove("./keytmp.pem")
    response_data = {
        "Status":"Successfully create new private key", 
        "Private_key": base64_encode,
    }
    return JSONResponse(content=response_data)