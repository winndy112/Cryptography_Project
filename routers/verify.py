# import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models import Base, Students, Ins, Quals
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from starlette.requests import Request
from fastapi.responses import JSONResponse
from certificate import parse_cert
import base64, hashlib, json, logging, qr, pickle, os
import digital_signature as dsa

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]   

class verifyRequest(BaseModel):
    file : str # base64 encode


@router.post("/verify")
async def verify_file(request: Request, db: db_dependency, form_data: verifyRequest):
    try:
        
        _file = form_data.file
        # check nội dung truyền vào
        if not _file:
            raise HTTPException(status_code=400, detail="Empty file")
        content = base64.b64decode(_file)

        # tạo cặp key ban đầu
        pair = dsa.digital_signature()
        
        # lấy certificate và signature từ trường metadata của file
        cert = pair.dettach_signature_and_cert(content)
        response_data = {}
        if pair.signature and cert:
            ca = dsa.digital_signature()
            # phân tích các trường của file certificate
            cert_info = parse_cert(cert)

            ''''
            xác thực chữ kí của root CA
            '''
            ca.load_CA_public_key("Root_CA/public.pem") # load public key của root CA
            signature_ca = cert_info["Signature"] # lấy chữ kí của root CA kí cert
            
            raw_signature_ca = bytes.fromhex(signature_ca.replace(":", ""))
            message = cert_info.copy() # extract message
            del message["Signature"]
            message["Public Key"] = base64.b64encode(pickle.dumps(cert_info["Public Key"])).decode('utf-8')
            message = json.dumps(message, default=str)
            
            #debugging
            # with open("test1.txt", "w") as file:
            #     file.write(message)

            hashed_message = hashlib.sha512(message.encode()).digest()
            
            # xác thực chữ kí của Root CA
            res = ca.pk.verify(hashed_message, raw_signature_ca)
    
            if (res == True):
                response_data["root_ca"] = True
                response_data["root_ca_name"] = cert_info["Issuer"]
            else: 
                response_data["root_ca"] = False
                return response_data
            
            '''
            Xác thực nơi cấp
            '''
            
            response_data["institution_name"] = cert_info.get("Subject")
            response_data["authority_person"] = cert_info["Author"]
            
            # lấy public key từ certificate
            pair.pk = cert_info["Public Key"]
            tmp = "test/tmp.pdf"
            # xóa cert/sign trong metadata 
            pair.remove_data_from_metadata(content, tmp)
            # xóa qr code trong pdf
            content =qr.remove_qr_code_from_pdf(tmp)
            # verify file
            out = "test/pdf_tmp.pdf"
            with open(out, "rb") as file:
                _content = file.read()
                verification_result = str(pair.verify(_content))
                response_data["result"] = verification_result
            os.remove(tmp)
            os.remove(out)
            #Return JSON response
            return JSONResponse(content=response_data)

        else:
            raise HTTPException(status_code=400, detail="Signature or certificate not found in the PDF")
    except Exception as e:
        logging.exception("Error during file verification:")
        raise HTTPException(status_code=500, detail=str(e))
