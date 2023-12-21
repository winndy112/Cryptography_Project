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
from starlette.requests import Request
import digital_signature as dsa
from fastapi import File, UploadFile
import digital_signature as dsa
import logging
from certificate import create_cert, parse_cert
router = APIRouter()
logging.basicConfig(level=logging.DEBUG)

@router.post("/verify")
async def verify_file(request: Request, file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="File is not a PDF")

        # Check if the file is empty
        if not file.file or not file.file.read(1):
            raise HTTPException(status_code=400, detail="Empty file")

        # Initialize the digital_signature object
        pair = dsa.digital_signature()
        
        # Get cert and signature from the document
        cert = pair.dettach_signature_and_cert(file)
        if pair.signature and cert:
            cert_info = parse_cert(cert)
            pair.pk = cert_info["Public Key"]

            # Perform digital signature verification
            verification_result = str(pair.verify(file))
            
            # Return JSON response
            response_data = {
                "result": verification_result,
                # "subject": cert_info["Subject"],
                # "author": cert_info["Author"]
            }
            return JSONResponse(content=response_data)

        else:
            raise HTTPException(status_code=400, detail="Signature or certificate not found in the PDF")
    except Exception as e:
        logging.exception("Error during file verification:")
        raise HTTPException(status_code=500, detail=str(e))
