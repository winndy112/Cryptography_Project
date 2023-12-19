import sys
sys.path.append('/falcon')
from falcon import falcon
import base64
import pickle
import fitz

# GLOBAL VARIABLES
KEY_LENGTH = 512


class digital_signature():
    '''
    khởi tạo
    '''
    def __init__(self):
        self.sk = None
        self.pk = None
        
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
        document = fitz.open(input_file)
        page = document[0]
        message = page.get_text()
        sig = self.sk.sign(message.encode())
        sign_b64 = base64.b64encode(sig)
        document.close()
        return sign_b64
    
    '''
    hàm xác thực chữ kí số dựa trên 3 input: chữ kí số encoded base64, file văn bằng cần xác thực và public key
    '''
    def verify(self, sign_b64: str, input_file: str) -> bool:
        document = fitz.open(input_file)
        page = document[0]
        message = page.get_text().encode()
        sign = base64.b64decode(sign_b64)
        return (self.pk.verify(message, sign))
    '''
    Hàm lưu key vào file pem
    '''
    def SaveSecret2Pem(self, filepath):
        falcon_public_key_begin = "-- Begin Falcon Private Key --\n"
        falcon_public_key_end = "\n-- End Falcon Private Key --\n"
        serialized_key = pickle.dumps(self.sk)
        encoded_key = base64.b64encode(serialized_key).decode('utf-8')
        with open(filepath, 'w') as file:
            file.write(falcon_public_key_begin)
            file.write(encoded_key)
            file.write(falcon_public_key_end)

    def SavePublic2Pem(self, filepath):
        falcon_public_key_begin = "-- Begin Falcon Public Key --\n"
        falcon_public_key_end = "\n-- End Falcon Public Key --\n"
        serialized_key = pickle.dumps(self.pk)
        encoded_key = base64.b64encode(serialized_key).decode('utf-8')
        with open(filepath, 'w') as file:
            file.write(falcon_public_key_begin)
            file.write(encoded_key)
            file.write(falcon_public_key_end)
    ''' 
    Hàm giải mã key từ file pem 
    '''
    def load_private_key(self, file_path):  
        try:
            with open(file_path, 'r') as file:
                encoded_secret_key = file.read()

            if encoded_secret_key.startswith("-- Begin Falcon Private Key --"):
                encoded_secret_key = encoded_secret_key.split("-- Begin Falcon Private Key --")[1]
            if encoded_secret_key.endswith("\n-- End Falcon Private Key --\n"):
                encoded_secret_key = encoded_secret_key.rsplit("\n-- End Falcon Private Key --\n", 1)[0]

            decoded_secret_key = base64.b64decode(encoded_secret_key)
            secret_key = pickle.loads(decoded_secret_key)
            self.sk = secret_key
        except Exception as e:
            print(f"Error loading secret key: {e}")

    def load_public_key(self, file_path):
        try:
            with open(file_path, 'r') as file:
                encoded_public_key = file.read()

            if encoded_public_key.startswith("-- Begin Falcon Public Key --"):
                encoded_public_key = encoded_public_key.split("-- Begin Falcon Public Key --")[1]
            if encoded_public_key.endswith("\n-- End Falcon Private Key --\n"):
                encoded_public_key = encoded_public_key.rsplit("\n-- End Falcon Private Key --\n", 1)[0]

            decoded_public_key = base64.b64decode(encoded_public_key)
            public_key = pickle.loads(decoded_public_key)
            self.pk = public_key
        except Exception as e:
            return f"Error loading public key: {e}"


# Example Usage:
# a = digital_signature()
# a.create_key()
# a.SaveSecret2Pem("Root_CA\\private.pem")
# a.SavePublic2Pem("Root_CA\\public.pem")
b = digital_signature()
b.load_private_key("Root_CA\\private.pem")
b.load_public_key("Root_CA\\public.pem")       
print(b.sk)
print(b.pk)