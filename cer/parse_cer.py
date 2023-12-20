import sys
sys.path.append('/falcon')
from falcon import falcon
import base64
import pickle

# Đường dẫn đến tệp cer
cer_file = "certificate.cer"


# Đọc nội dung tệp cer
with open(cer_file, "rb") as file:
    # Read the content excluding "BEGIN CERTIFICATE" and "END CERTIFICATE" lines
    cert_base64 = file.read().replace(b"---BEGIN CERTIFICATE---", b"").replace(b"---END CERTIFICATE---", b"").strip()

# Giải mã base64 để nhận lại nội dung chứng chỉ
cert_content = base64.b64decode(cert_base64).decode("utf-8")

# Phân tích thông tin từ nội dung chứng chỉ
lines = cert_content.split("\n")
username = lines[0].split(": ")[1]
address = lines[1].split(": ")[1]
public_key = lines[2].split(": ")[1]

decoded_public_key = base64.b64decode(public_key)
restored_key = pickle.loads(decoded_public_key)


# In thông tin
print(f"Hiệu trưởng: {username}")
print(f"Trường: {address}")
#print(f"Raw Public Key: {decoded_public_key} \n")
print(f"Raw Public Key: {restored_key} \n")
#print(f"en code Public Key: {public_key}")
