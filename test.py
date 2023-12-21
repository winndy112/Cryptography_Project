# from OpenSSL import *
# import OpenSSL

# def createKeyPair(type, bits):
#     """
#     Create a public/private key pair
#     Arguments: Type - Key Type, must be one of TYPE_RSA and TYPE_DSA
#                bits - Number of bits to use in the key (1024 or 2048 or 4096)
#     Returns: The public/private key pair in a PKey object
#     """
#     pkey = OpenSSL.crypto.PKey()
#     pkey.generate_key(type, bits)
#     return pkey

# def create_self_signed_cert(pKey):
#     """Create a self signed certificate. This certificate will not require to be signed by a Certificate Authority."""
#     # Create a self signed certificate
#     cert = OpenSSL.crypto.X509()
#     # Common Name (e.g. server FQDN or Your Name)
#     cert.get_subject().CN = "BASSEM MARJI"
#     # Serial Number
#     cert.set_serial_number(int(time.time() * 10))
#     # Not Before
#     cert.gmtime_adj_notBefore(0)  # Not before
#     # Not After (Expire after 10 years)
#     cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
#     # Identify issue
#     cert.set_issuer((cert.get_subject()))
#     cert.set_pubkey(pKey)
#     cert.sign(pKey, 'md5')  # or cert.sign(pKey, 'sha256')
#     return cert

# def load():
#     """Generate the certificate"""
#     summary = {}
#     summary['OpenSSL Version'] = OpenSSL.__version__
#     # Generating a Private Key...
#     key = createKeyPair(OpenSSL.crypto.TYPE_RSA, 1024)
#     # PEM encoded
#     with open('.\static\private_key.pem', 'wb') as pk:
#         pk_str = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
#         pk.write(pk_str)
#         summary['Private Key'] = pk_str
#     # Done - Generating a private key...
#     # Generating a self-signed client certification...
#     cert = create_self_signed_cert(pKey=key)
#     with open('.\static\certificate.cer', 'wb') as cer:
#         cer_str = OpenSSL.crypto.dump_certificate(
#             OpenSSL.crypto.FILETYPE_PEM, cert)
#         cer.write(cer_str)
#         summary['Self Signed Certificate'] = cer_str
#     # Done - Generating a self-signed client certification...
#     # Generating the public key...
#     with open('.\static\public_key.pem', 'wb') as pub_key:
#         pub_key_str = OpenSSL.crypto.dump_publickey(
#             OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())
#         #print("Public key = ",pub_key_str)
#         pub_key.write(pub_key_str)
#         summary['Public Key'] = pub_key_str
#     # Done - Generating the public key...
#     # Take a private key and a certificate and combine them into a PKCS12 file.
#     # Generating a container file of the private key and the certificate...
#     p12 = OpenSSL.crypto.PKCS12()
#     p12.set_privatekey(key)
#     p12.set_certificate(cert)
#     open('.\static\container.pfx', 'wb').write(p12.export())
#     # You may convert a PKSC12 file (.pfx) to a PEM format
#     # Done - Generating a container file of the private key and the certificate...
#     # To Display A Summary
#     print("## Initialization Summary ##################################################")
#     print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
#     print("############################################################################")
#     return True


# import fitz  # PyMuPDF

# def attach_image_to_pdf(pdf_path, image_path, output_pdf_path, x, y):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)

#     # Open the image file
#     image_document = fitz.open(image_path)

#     # Get the first page of the PDF document
#     pdf_page = pdf_document[0]

#     # Get the first page of the image document
#     image_page = image_document[0]

#     # Copy the image to the PDF page
#     pdf_page.insert_image((x, y), image_page)

#     # Save the modified PDF
#     pdf_document.save(output_pdf_path)
    
#     # Close the PDF and image documents
#     pdf_document.close()
#     image_document.close()

# # Example usage:
# input_file = "./test/Projects-Topics.pdf"
# qr_code_path = './image/qrcode.png'
# output_file = "./test/signed_Projects-Topics.pdf"
# x_position = 0  # Adjust the X position of the image
# y_position = 0  # Adjust the Y position of the image

# attach_image_to_pdf(input_file, qr_code_path, output_file, x_position, y_position)


# import PyPDF2
# pdf_file = "test/signed_qual.pdf"

# with open(pdf_file, 'rb') as file:
#     #signature = 'test'
#     # Create a PDF reader
#     pdf_reader = PyPDF2.PdfReader(file)
#     # Get the document information (metadata)
#     meta = pdf_reader.metadata
#     print(meta)
#     # pdf_writer = PyPDF2.PdfWriter()
#     # xmp_metadata = f"signature"
#     # pdf_writer.add_metadata({PyPDF2.generic.NameObject('/Signature'): xmp_metadata.encode()})
#     # with open('output.pdf', 'wb') as fout:
#     #             pdf_writer.write(fout)
# import base64
# import pickle
# def gen_cert(cer_file):
#     # Đường dẫn đến tệp cer
#     #cer_file = "certificate.pem"
#     # Đọc nội dung tệp cer
#     with open(cer_file, "rb") as file:
#         cert_base64 = file.read().replace(b"---BEGIN CERTIFICATE---", b"").replace(b"---END CERTIFICATE---", b"").strip()

#         # Giải mã base64 để nhận lại nội dung chứng chỉ
#     cert_content = base64.b64decode(cert_base64).decode("utf-8")
#     print(cert_content)
#     # Phân tích thông tin từ nội dung chứng chỉ
#     lines = cert_content.split("\n")
#     username = lines[0].split(": ")[1]
#     address = lines[1].split(": ")[1]
#     public_key = lines[2].split(": ")[1]
#     decoded_public_key = base64.b64decode(public_key)
#     print(decoded_public_key)
#     # Now you can use the decoded_public_key directly without pickling it
#     # If you still want to pickle it, use pickle.dumps, not pickle.loads
#     restored_key = pickle.loads(decoded_public_key)

#     # In thông tin
#     print(f"Hiệu trưởng: {username}")
#     print(f"Trường: {address}")
#     #print(f"Raw Public Key: {decoded_public_key} \n")
#     print(f"Raw Public Key: {restored_key} \n")
#     #print(f"en code Public Key: {public_key}")



# import base64

# # Đường dẫn đến tệp tin chứa public key
# public_key_file = "Root_CA/public.pem"

# # Đọc public key từ tệp tin
# with open(public_key_file, "r") as file:
#     public_key = file.read().strip()

# # Tạo thông tin chứng chỉ
# username = "Nguyễn Hoàng Tú Anh"
# address = "UIT"

# # Tạo nội dung tệp cer
# cert_content = f"Username: {username}\nAddress: {address}\nPublic Key: {public_key}"
# print(cert_content)
# # Chuyển đổi nội dung cert thành base64
# cert_base64 = base64.b64encode(cert_content.encode())

# begin = b"---BEGIN CERTIFICATE---\n"
# end = b"\n---END CERTIFICATE---\n"

# # Lưu tệp cer
# with open("certificate.cer", "wb") as cert_file:
#     cert_file.write(begin)
#     cert_file.write(cert_base64)
#     cert_file.write(end)

# content = {

# }
# gen_cert("certificate.cer")
# # '''
# # Tạo secret key và public key cho 
# # '''
import digital_signature as dsa
import qr
from certificate import create_cert, parse_cert
from datetime import timedelta, datetime
a = dsa.digital_signature()
# a.load_public_key("Root_CA\\public.pem")
# a.load_private_key("Root_CA\\private.pem")
a.create_key()
infor = {
        "Version": 1, # có thể nâng cấp kiểm tra version trước đó
        "Issuer": "Root CA Signing and Verify System",
        "Subject ": "create_user_request.institutionName",
        "Author": "create_user_request.authority_person",
        "Public Key Algorithm": "Falcon",
        "Public Key": None,
        "Valididy" : {
            "Not Before" : datetime.now().isoformat(),
            "Not After" : (datetime.now() + timedelta(days=365 * 2)).isoformat()
        },
        "Signature Algorithm" : "sha512withFalcon",
        "Signature" : None
    }
infor["Public Key"] = a.pk
print(infor)
# # print(a.sk)
# # print(a.pk)

# # '''
# # test sign và add vào qr
# # '''
# doc = "test/test.pdf"
# qr_code_path = './image/qrcode.png'
# signed_doc = "test/signed_qual.pdf"
# a.signing_pdf(doc)

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
# a.add_data_to_metadata(doc, "./cert.pem", signed_doc)
# qr.generateQr_and_add_to_pdf( a.signature, signed_doc, qr_code_path)
# cert = a.dettach_signature_and_cert(signed_doc)
# cert_info = parse_cert(cert)
# a.pk = cert_info["Public Key"]
# veri = a.verify("test\\signed_qual.pdf")
# print(veri)




# '''
# test verify
# '''

# sign_doc = "test\signed_qual.pdf"
# qr.remove_qr_code_from_pdf(sign_doc, "test\\verify_doc.pdf")
# a.dettach_signature(sign_doc)

# print(veri)
# h còn tạo cert thử với in mã qr vào document