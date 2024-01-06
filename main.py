import digital_signature as dsa
# thư viện chuyển đối tượng thành bytes
import pickle
import PyPDF2
from fastapi import FastAPI
import models
from routers import create_key, get, verify, signFile
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
app = FastAPI()


# Thêm phần trung gian CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Cập nhật địa chỉ frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine) # Tạo một bảng ghi from fastapi import FastAPI

app.include_router(get.router)
app.include_router(create_key.router)
app.include_router(verify.router)
app.include_router(signFile.router)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<html><body><h1>FastAPI is running!</h1></body></html>"
