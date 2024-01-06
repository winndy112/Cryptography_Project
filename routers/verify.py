# import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models import Base, Students, Ins, Quals
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
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
    pubKey: str #base64 encode

@router.post("/verify")
async def verify_file(db: db_dependency, form_data: verifyRequest):
    try:
        # check nội dung truyền vào
        if not form_data.file or not form_data.pubKey:
            raise HTTPException(status_code=400, detail="Empty file")
        content = base64.b64decode(form_data.file)
        pubkey = base64.b64decode(form_data.pubKey)
    
        # load public key
        pair = dsa.digital_signature()
        pair.load_public_key(pubkey)

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

                return JSONResponse(content=response_data)
            
            '''
            Xác thực nơi cấp
            '''
            
            
            ins = db.query(Ins).filter(Ins.institution_name == cert_info.get("Subject"), Ins.authority_person == cert_info["Author"]).first()

            if not ins:
                response_data["result"] = False
                response_data["reason"] = "Không có nhà phát hành " + cert_info.get("Subject")
                return JSONResponse(content=response_data)
            
            ins_pubkey = dsa.digital_signature()
            ins_pubkey.load_public_key(ins.public_file)

            # nếu public được submit lên đúng nhà phát hành
            if str(pair.pk) == str(cert_info["Public Key"]) == str(ins_pubkey.pk):
                response_data["institution_name"] = ins.institution_name
                response_data["authority_person"] = ins.authority_person

            else:
                response_data["result"] = False
                response_data["reason"] = "Không đúng Public key"
            
                return JSONResponse(content=response_data)

            tmp = "test/tmp.pdf"
            # xóa cert/sign trong metadata 
            pair.remove_data_from_metadata(content, tmp)
            # xóa qr code trong pdf
            content =qr.remove_qr_code_from_pdf(tmp)
            # verify file
            out = "test/pdf_tmp.pdf"
            with open(out, "rb") as file:
                _content = file.read()
                verification_result = pair.verify(_content)
                response_data["result"] = verification_result
                if verification_result == False:
                    response_data["reason"] = "Signature hoặc nội dung văn bằng không hợp lệ!"
            os.remove(tmp)
            os.remove(out)
            #Return JSON response
            return JSONResponse(content=response_data)

        else:
            raise HTTPException(status_code=400, detail="Signature or certificate not found in the PDF")
    except Exception as e:
        logging.exception("Error during file verification:")
        raise HTTPException(status_code=500, detail=str(e))
