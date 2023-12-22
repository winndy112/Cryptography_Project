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
import re
import qr
from models import Students, Ins, Quals
import digital_signature as dsa
import certificate

router = APIRouter()

SECRET_KEY = '5d3711a26b488b38642c948a7bc8fa09fe9ba78a2d6b57cac46a34bb0f840147' # key from unique user
ALGORITHM = "HS256" # algorithm

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # instace to hashing password

logging.basicConfig(level=logging.DEBUG) # log dùng để debug

'''
Form data request khi user muốn sign up
'''
class CreateUserRequest(BaseModel):
    institutionName: str
    authority: str
    signupEmail: str
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


def authenticate_user(email_address: str, password: str, db):
    user = db.query(Ins).filter(Ins.email_address == email_address).first()
    
    if not user:
        return False
    # the password not match
    if not bcrypt_context.verify(password, user.hashed_password): # compare beetween input and database
        return False
    return user

def create_access_token(email_address: str, institution_id: int, expires_delta: timedelta):

    encode = {'sub': email_address}
    if institution_id:
        encode.update({'id': institution_id})
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


'''
hàm check format của email
'''
def is_valid_email(email):
    # Using a simple regular expression for basic email format validation
    email_pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(email_pattern, email))

@router.post("/auth")
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    
    if not is_valid_email(create_user_request.signupEmail):
        raise HTTPException(status_code=400, detail="Invalid email format")
    # kiểm tra email đã được đăng kí chưa
    existing_user = db.query(Ins).filter(Ins.email_address == create_user_request.signupEmail).first()
    if existing_user:
        raise HTTPException(detail="Email already exists", status_code=400)
    
    '''
    cần dùng tpm
    '''
    # cặp key của root CA 
    root_ca = dsa.digital_signature()
    root_ca.load_CA_private_key("Root_CA/private.pem")
    
    # tạo cặp key cho người dùng
    pair = dsa.digital_signature()
    pair.create_key()
    # tạo certificate file
    infor = {
        "Version": "1", # có thể nâng cấp kiểm tra version trước đó
        "Issuer": "Root CA Signing and Verify System",
        "Subject": create_user_request.institutionName,
        "Author": create_user_request.authority,
        "Public Key Algorithm": "Falcon",
        "Public Key": None,
        "Validity" : {
            "Not Before" : datetime.now().isoformat(),
            "Not After" : (datetime.now() + timedelta(days=365 * 2)).isoformat()
        },
        "Signature Algorithm" : "sha512withFalcon"
    }
    
    # lấy public key của user thêm vào certificate
    serialized_key = pickle.dumps(pair.pk)
    encoded_key = base64.b64encode(serialized_key).decode('utf-8')
    infor["Public Key"] = encoded_key
    message = json.dumps(infor, default=str)
    with open("test.txt", "w") as file:
        file.write(message)
    hashed_message = hashlib.sha512(message.encode()).digest()
    # tính signature các thông tin của user bằng private key của root CA
    sig = root_ca.sk.sign(hashed_message)
    hex_signature = "".join(f"{byte:02x}:" for byte in sig)
    infor["Signature"] = hex_signature
    # tạo một file cert tạm
    certificate.create_cert(infor, "cert/temp.pem")
    with open(r"cert/temp.pem", "rb") as f:
        cert = f.read()
    
    # thêm ins và certificate của nó vào database
    create_user_model = Ins( institution_name =create_user_request.institutionName,
                                authority_person = create_user_request.authority,
                                email_address = create_user_request.signupEmail,
                                # hash password trước khi lưu vào database
                                hashed_password= bcrypt_context.hash(create_user_request.password),
                                certificate_file = cert
                            )
    
    db.add(create_user_model) # insert
    db.commit() # commit insert process
    file = pair.SaveSecret2Pem("./keytmp.pem")
    with open("./keytmp.pem", "rb") as file:
        content = file.read()
    base64_encode = base64.b64encode(content).decode("utf-8")  
    response_data = {
        "Status":"Successfully signed up new institution", 
        "Private_key": base64_encode,
    }
    os.remove("cert/temp.pem")
    os.remove("./keytmp.pem")
    return JSONResponse(content=response_data)

@router.post("/token")
async def login_for_access_token(request: Request, db: db_dependency):
    form_data = await request.json()

    user = authenticate_user(form_data["email_address"], form_data["password"], db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email_address, user.institution_id, timedelta(minutes=20))
    return {'access_token': token, "token_type": "bearer"}

