import sys
sys.path.append('/falcon')
import qr
from falcon import falcon
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

KEY_LENGTH = 512

class digital_signature():
    '''
    tạo pair public key và private key sử dụng FALCON sheme
    '''
    def create_key(self) -> (falcon.SecretKey, falcon.PublicKey):
        self.sk = falcon.SecretKey(KEY_LENGTH)
        self.pk = falcon.PublicKey(self.sk)
        #byte_key = falcon.PublicKey.to_bytes(self.pk)
        #save_public_key_to_pem(byte_key, 'private_key.pem')

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
    hàm xác thực chữ kí số dựa trên 3 input: chữ kí số encode base64, file văn bằng cần xác thực và public key
    '''

    def verify(self, sign_b64: str, input_file: str) -> bool:
        file = open(input_file, "rb")
        message= file.read()
        sign = base64.b64decode(sign_b64)
        return (self.pk.verify(message, sign))


a = digital_signature()
a.create_key()

input_file = "test\\Projects-Topics.pdf"

sign_a = a.signing_pdf(input_file)

qr.generate_qr(sign_a, './qrcode.png')

veri = a.verify(sign_a, input_file)

print(veri)

# h còn tạo cert thử với in mã qr vào document
