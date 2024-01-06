import sys
sys.path.append('/falcon')
from falcon import falcon
import base64, pickle, fitz
import pickle
import fitz
import PyPDF2 
import io
import os

# GLOBAL VARIABLES
KEY_LENGTH = 512


class digital_signature():
    '''
    khởi tạo
    '''
    def __init__(self):
        self.signature = None
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
    
    def signing_pdf(self, input_file: bytes):
        tmp = "./test/_tmp.pdf" 
        with open(tmp, "wb") as file:
            file.write(input_file)
        doc = fitz.open(tmp)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        sig = self.sk.sign(text.encode("utf-8"))
        sign_b64 = base64.b64encode(sig).decode()
        self.signature = sign_b64
        doc.close()
        os.remove(tmp)

    '''
    hàm xác thực chữ kí số dựa trên 3 input: chữ kí số encoded base64, file văn bằng cần xác thực và public key
    '''
    def verify(self, input_file: bytes) -> bool:
        if not input_file:
            return False  
        tmp = "./test/_tmp.pdf" 
        with open(tmp, "wb") as file:
            file.write(input_file)
        doc = fitz.open(tmp)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        sign = base64.b64decode(self.signature)
        # Trả về kết quả xác minh
        result = self.pk.verify(text.encode("utf-8"), sign)
        doc.close()
        os.remove(tmp)
        return result
    '''
    Hàm thêm chữ kí và văn bằng vào trường metadata của văn bằng pdf
    '''
    
    def add_data_to_metadata(self, pdf_bytes: bytes, cert_file: bytes, output_file: str):
        try:
            writer = PyPDF2.PdfWriter()
            pdf_stream = io.BytesIO(pdf_bytes)
            reader =PyPDF2.PdfReader(pdf_stream)
            metadata= reader.metadata
            extracted_metadata = {}
            extracted_metadata['/Signature'] = self.signature
            extracted_metadata['/Certificate'] = cert_file.decode()
            writer.append_pages_from_reader(reader)
            for key in metadata:
                writer.add_metadata({PyPDF2.generic.create_string_object(key): PyPDF2.generic.create_string_object(str(metadata[key]))})
            for key in extracted_metadata:
                writer.add_metadata({PyPDF2.generic.create_string_object(key): PyPDF2.generic.create_string_object(str(extracted_metadata[key]))})
            with open(output_file, 'wb') as fout:
                writer.write(fout)
        except Exception as e:
            print(f"Error adding signature to PDF metadata: {e}")

    def dettach_signature_and_cert(self, input_pdf: bytes):
        pdf_stream = io.BytesIO(input_pdf)
        pdf_reader =PyPDF2.PdfReader(pdf_stream)
        meta = pdf_reader.metadata
        if "/Signature" in meta:
            self.signature = (str(meta['/Signature']).encode()) 
        return meta["/Certificate"]
        
    def remove_data_from_metadata(self, input: bytes, output_file: str):
        try:
            input_file = io.BytesIO(input)
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            metadata= reader.metadata
            writer.append_pages_from_reader(reader)
            for key in metadata:
                if key == "/Signature" or key == "/Certificate":
                    continue
                writer.add_metadata({PyPDF2.generic.create_string_object(key): PyPDF2.generic.create_string_object(str(metadata[key]))})
            with open(output_file, 'wb') as fout:
                writer.write(fout)
        except Exception as e:
            print(f"Error removing metadata: {e}")
    
    
    '''
    Hàm lưu key vào file pem
    '''
    def SaveSecret2Pem(self, filepath: str):
        falcon_Private_key_begin = "------ Begin Falcon Private Key ------\n"
        falcon_Private_key_end = "\n------ End Falcon Private Key ------\n"
        serialized_key = pickle.dumps(self.sk)
        encoded_key = base64.b64encode(serialized_key).decode('utf-8')
        with open(filepath, 'w') as file:
            file.write(falcon_Private_key_begin)
            file.write(encoded_key)
            file.write(falcon_Private_key_end)

    def SavePublic2Pem(self, filepath: str):
        falcon_public_key_begin = "------ Begin Falcon Public Key ------\n"
        falcon_public_key_end = "\n------ End Falcon Public Key ------\n"
        serialized_key = pickle.dumps(self.pk)
        encoded_key = base64.b64encode(serialized_key).decode('utf-8')
        with open(filepath, 'w') as file:
            file.write(falcon_public_key_begin)
            file.write(encoded_key)
            file.write(falcon_public_key_end)

    ''' 
    Hàm giải mã key từ bytes được truyền về frontend
    '''
    def load_private_key(self, file: bytes):  
        try:
            encoded_secret_key = file.decode("utf-8")
            if encoded_secret_key.startswith("------ Begin Falcon Private Key ------\r\n"):
                encoded_secret_key = encoded_secret_key.split("------ Begin Falcon Private Key ------\r\n")[1]
            if encoded_secret_key.endswith("\r\n------ End Falcon Private Key ------\r\n"):
                encoded_secret_key = encoded_secret_key.rsplit("\r\n------ End Falcon Private Key ------\r\n", 1)[0]
            decoded_secret_key = base64.b64decode(encoded_secret_key)   
            secret_key = pickle.loads(decoded_secret_key)
            self.sk = secret_key
            self.pk = falcon.PublicKey(self.sk)
        except Exception as e:
            print(f"Error loading secret key: {e}")
    
    def load_public_key(self, file: bytes):  
        try:
            encoded_public_key = file.decode("utf-8")
            if encoded_public_key.startswith("------ Begin Falcon Public Key ------\r\n"):
                encoded_public_key = encoded_public_key.split("------ Begin Falcon Public Key ------\r\n")[1]
            if encoded_public_key.endswith("\r\n------ End Falcon Public Key ------\r\n"):
                encoded_public_key = encoded_public_key.rsplit("\r\n------ End Falcon Public Key ------\r\n", 1)[0]
            decoded_public_key = base64.b64decode(encoded_public_key)   
            public = pickle.loads(decoded_public_key)
            self.pk = public
        except Exception as e:
            print(f"Error loading public key: {e}")

    def load_CA_public_key(self, file_path):
        try:
            with open(file_path, 'r') as file:
                encoded_public_key = file.read()

            if encoded_public_key.startswith("------ Begin Falcon Public Key ------\n"):
                encoded_public_key = encoded_public_key.split("------ Begin Falcon Public Key ------\n")[1]
            if encoded_public_key.endswith("\n------ End Falcon Public Key ------\n"):
                encoded_public_key = encoded_public_key.rsplit("\n------ End Falcon Public Key ------\n", 1)[0]

            decoded_public_key = base64.b64decode(encoded_public_key)
            public_key = pickle.loads(decoded_public_key)
            self.pk = public_key
        except Exception as e:
            return f"Error loading public key: {e}"
        
    '''
    Hàm giải mã key từ file pem
    '''
    def load_CA_private_key(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                encoded_private_key = file.read()
            if encoded_private_key.startswith("------ Begin Falcon Private Key ------\n"):
                encoded_private_key = encoded_private_key.split("------ Begin Falcon Private Key ------\n")[1]
            if encoded_private_key.endswith("\n------ End Falcon Private Key ------\n"):
                encoded_private_key = encoded_private_key.rsplit("\n------ End Falcon Private Key ------\n", 1)[0]
            decoded_private_key = base64.b64decode(encoded_private_key)
            private_key = pickle.loads(decoded_private_key)
            self.sk = private_key
        except Exception as e:
            return f"Error loading private key: {e}"
        