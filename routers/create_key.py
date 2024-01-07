# import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from fastapi.responses import JSONResponse
import base64,os
import digital_signature as dsa


router = APIRouter()

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