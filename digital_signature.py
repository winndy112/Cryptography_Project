import sys
sys.path.append('/falcon')
import qr
from falcon import falcon
import base64


# GLOBAL VARIABLES
KEY_LENGTH = 512


def save_bytes_to_pem(byte_string, file_path, pem_type):
    pem_data = b"-----BEGIN " + pem_type.encode() + b"-----\n"
    pem_data += base64.b64encode(byte_string) + b"\n"
    pem_data += b"-----END " + pem_type.encode() + b"-----\n"

    with open(file_path, 'wb') as pem_file:
        pem_file.write(pem_data)

class digital_signature():
    '''
    tạo pair public key và private key sử dụng FALCON sheme
    '''
    def create_key(self) -> (falcon.SecretKey, falcon.PublicKey):
        self.sk = falcon.SecretKey(KEY_LENGTH)
        self.pk = falcon.PublicKey(self.sk)

    '''
    Kí chữ kí số cho văn bằng
    Trả về chữ kí số được mã hóa Base64
    '''

    def signing_pdf(self, input_file: str) -> str:
        with open(input_file, "rb") as file:
            message = file.read()
        sig = self.sk.sign(message)
        sign_b64 = base64.b64encode(sig)
        return sign_b64
    
    '''
    hàm xác thực chữ kí số dựa trên 3 input: chữ kí số encoded base64, file văn bằng cần xác thực và public key
    '''

    def verify(self, sign_b64: str, input_file: str) -> bool:
        file = open(input_file, "rb")
        message= file.read()
        sign = base64.b64decode(sign_b64)
        return (self.pk.verify(message, sign))






