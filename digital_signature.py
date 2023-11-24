import sys
sys.path.append('/falcon')
from falcon import falcon
import base64

KEY_LENGTH = 512
class digital_signature():

    def create_key(self) -> (falcon.SecretKey, falcon.PublicKey):
        self.sk = falcon.SecretKey(KEY_LENGTH)
        self.pk = falcon.PublicKey(self.sk)
        #return (sk, pk)

    def signing_pdf(self, input_file: str) -> str:
        with open(input_file, "rb") as file:
            message = file.read()
        sig = self.sk.sign(message)
        sign_b64 = base64.b64encode(sig)
        #print(sign_b64)
        return sign_b64
    # print(sign_b64)
    def verify(self, sign_b64: str, input_file: str) -> bool:
        file = open(input_file, "rb")
        message= file.read()
        sign = base64.b64decode(sign_b64)
        return (self.pk.verify(message, sign))


a = digital_signature()
a.create_key()

input_file = "test\\Projects-Topics.pdf"

sign_a = a.signing_pdf(input_file)
with open("sign.bin", "w") as file:
    file.write(sign_a.decode())

veri = a.verify(sign_a, input_file)

print(veri)

# h còn tạo cert thử với in mã qr vào document

