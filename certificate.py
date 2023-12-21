import base64
import sys
sys.path.append('/falcon')
from falcon import falcon
import base64
import pickle
'''
Format của certificate
'''
certificate_format = {
        "Serial Number": None,
        "Issuer": None,
        "Subject ": None,
        "Author": None,
        "Public Key": None,
        "Valididy" : {
            "Not Before" : None,
            "Not After" : None
        },
        "Signature Algorithm" : None,
        "Signature" : None
    }
'''
Hàm tạo certificate dựa trên format 
'''
def create_cert(public_file: str, info: dict, cert_file: str):
    # Đọc public key từ tệp tin
    with open(public_file, "r") as file:
        public_key = file.read().strip()
    public_key = public_key.replace("\n------ End Falcon Public Key ------", '')
    info["Public Key"] = public_key.replace('------ Begin Falcon Public Key ------\n', '')
    
    # Tạo nội dung tệp cer
    cert_content = "\n".join([f"{key}: {value}" for key, value in info.items()])
    # Chuyển đổi nội dung cert thành base64
    cert_base64 = base64.b64encode(cert_content.encode("utf-8"))

    begin = b"---BEGIN CERTIFICATE---\n"
    end = b"\n---END CERTIFICATE---\n"

    # Lưu tệp cer
    with open(cert_file, "wb") as cert_file:
        cert_file.write(begin)
        cert_file.write(cert_base64)
        cert_file.write(end)

'''
Hàm phân tích cert dựa trên format
'''
def parse_cert(cert_file):
    # Đọc nội dung tệp cer
    with open(cert_file, "rb") as file:
        cert_base64 = file.read().replace(b"---BEGIN CERTIFICATE---", b"").replace(b"---END CERTIFICATE---", b"").strip()

    # Giải mã base64 để nhận lại nội dung chứng chỉ
    cert_content = base64.b64decode(cert_base64).decode("utf-8")

    # Phân tích thông tin từ nội dung chứng chỉ thành dictionary
    cert_info = certificate_format
    lines = cert_content.split("\n")
    # print(lines)
    for line in lines:
        #print(line)
        key, value = line.split(": ", 1)
        if key == "Validity":
            validity_dict = eval(value)
            cert_info["Valididy"]["Not Before"] = validity_dict.get("Not Before")
            certificate_format["Valididy"]["Not After"] = validity_dict.get("Not After")
        cert_info[key] = value
    # print(cert_info)
    decoded_public_key = base64.b64decode(str(cert_info['Public Key']).encode())
    
    restored_key = pickle.loads(decoded_public_key)
    cert_info["Public Key"] = restored_key
    return cert_info




'''
Testing
'''
# certificate_info = {
#         "Serial Number": "123",
#         "Issuer": "Nhóm 5",
#         "Subject ": "Toeic",
#         "Author": "Nguyễn Văn A",
#         "Public Key": None,
#         "Valididy" : {
#             "Not Before" : " Sep 23 00:00:00 2023 GMT",
#             "Not After" : "Dec 22 23:59:59 2023 GMT"
#         },
#         "Signature Algorithm" : "sha256WithRSAEncryption",
#         "Signature" : "testing"
#     }
# create_cert("public.pem", certificate_info, "./cert.pem")
# print(parse_cert( "./cert.pem"))

