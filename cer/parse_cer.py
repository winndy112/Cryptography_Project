import sys
sys.path.append('/falcon')
from falcon import falcon
import base64
import pickle

# Đường dẫn đến tệp cer
cer_file = "certificate.cer"

# Đọc nội dung tệp cer
with open(cer_file, "rb") as file:
    cert_base64 = file.read().replace(b"---BEGIN CERTIFICATE---", b"").replace(b"---END CERTIFICATE---", b"").strip()

# Giải mã base64 để nhận lại nội dung chứng chỉ
cert_content = base64.b64decode(cert_base64).decode("utf-8")

# Phân tích thông tin từ nội dung chứng chỉ thành dictionary
cert_info = {}
lines = cert_content.split("\n")
for line in lines:
    key, value = line.split(": ")
    cert_info[key] = value
    
decoded_public_key = base64.b64decode(cert_info['Public Key'])
restored_key = pickle.loads(decoded_public_key)

# Check bằng cách in thử thông tin từ dictionary
#print(f"Hiệu trưởng: {cert_info['Username']}")
#print(f"Trường: {cert_info['Address']}")
#print(f"Raw Public Key: {restored_key} \n")
