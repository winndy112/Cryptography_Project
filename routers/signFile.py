# import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
import logging
from datetime import timedelta, datetime, date
from fastapi.responses import JSONResponse
import qr, re, os, base64, pickle, json, hashlib
from models import Students, Ins, Quals
import digital_signature as dsa
import certificate

router = APIRouter()

'''
Form data request khi user muốn kí văn bằng
'''
class SignFileRequest(BaseModel):
    ins: str
    authority: str
    email: str
    school: str
    studentName: str
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
def is_valid_email(email):
    # Using a simple regular expression for basic email format validation
    email_pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(email_pattern, email))
    
@router.post("/sign_file")
async def sign_file(request: Request, db: db_dependency, form_data: SignFileRequest):   
    try:
        pdf_tmp =  "test/tmp.pdf"
        image_tmp = "image/qrcode.png"

        _ins_name = form_data.ins
        _auth = form_data.authority
        _email = form_data.email
        _school = form_data.school
        _student_name = form_data.studentName
       
        input_file = form_data.inputFile #base64
        private_key = form_data.privateKey # base64
        if not is_valid_email(_email):
            raise HTTPException(status_code=400, detail="Invalid email format")
        pair = dsa.digital_signature()
        private_key = base64.b64decode(private_key)
        pair.load_private_key(private_key)
        # check nơi phát hành
        ins = db.query(Ins).filter(Ins.institution_name == _ins_name, Ins.authority_person == _auth,
                                   Ins.email_address == _email).first()
        if not ins:
            root_ca = dsa.digital_signature()
            root_ca.load_CA_private_key("Root_CA/private.pem")
    
            # tạo certificate file
            infor = {
                "Version": "1", # có thể nâng cấp kiểm tra version trước đó
                "Issuer": "Root CA Signing and Verify System",
                "Subject": _ins_name,
                "Author": _auth,
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
            hashed_message = hashlib.sha512(message.encode()).digest()
            # tính signature các thông tin của user bằng private key của root CA
            sig = root_ca.sk.sign(hashed_message)
            hex_signature = "".join(f"{byte:02x}:" for byte in sig)
            infor["Signature"] = hex_signature
            # tạo một file cert tạm
            certificate.create_cert(infor, "cert/temp.pem")
            pair.SavePublic2Pem("./key.pem")
            with open("./key.pem", "rb") as file:
                pubkey = file.read()
            with open(r"cert/temp.pem", "rb") as f:
                cert = f.read()
            ins = Ins(institution_name = _ins_name,authority_person = _auth, email_address=_email, public_file = pubkey, certificate_file = cert)
            db.add(ins)
            db.commit()
            db.refresh(ins)
            os.remove("./key.pem")
            os.remove("cert/temp.pem")

        # check xem student đã có trong database chưa
        student = db.query(Students).filter(Students.school == _school,
                                            Students.student_name == _student_name).first()
        
        if not student:
            # If the student is not in the database, add them
            student = Students(school=_school, student_name=_student_name)
            db.add(student)
            db.commit()
            db.refresh(student)
        
        # kí file
        input_bytes = base64.b64decode(input_file)
        pair.signing_pdf(input_bytes)
        
        # thêm certificate và signature vào file metadata của pdf
        pair.add_data_to_metadata(input_bytes, ins.certificate_file, pdf_tmp)
        with open(pdf_tmp, "rb") as file:
            byte = file.read()
        # thêm qr code vào pdf
        data = str(student.id_sv) + ' | ' + student.school + ' | ' + student.student_name
        pdf_output:bytes = qr.generateQr_and_add_to_pdf(data + ' | ' + pair.signature, byte, image_tmp)
        # lưu vào database
        qualification = Quals(
            id_sv=student.id_sv,
            issue_date=date.today(),
            expiration_date=date.today() + timedelta(days=365),  # văn bằng có hiêu lực 1 năm
            institution_id= ins.institution_id,
            pdf_file=pdf_output,
        )
        db.add(qualification)
        db.commit()

        # dữ liệu trả về
        pdf_output_base64 = base64.b64encode(pdf_output).decode('utf-8')
        response_json = {
            "pdf_content": pdf_output_base64,
            "nhaPhatHanh": ins.institution_name,
            "nguoiKi" : ins.authority_person,
            "id_sv" : student.id_sv
        }
        
        os.remove(pdf_tmp)
        os.remove(image_tmp)
        # Return the response
        return JSONResponse(content=response_json)
    except Exception as e:
        logging.exception("An error occurred during file signing:")
        raise HTTPException(status_code=500, detail="Internal Server Error")