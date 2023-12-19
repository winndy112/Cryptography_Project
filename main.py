import digital_signature as dsa
import qr 
# thư viện chuyển đối tượng thành bytes
import pickle
'''
Tạo secret key và public key cho 
'''

b = dsa.digital_signature()
b.load_public_key("Root_CA\\public.pem")
b.load_private_key("Root_CA\\private.pem")
print(b.sk)
'''
test sign
'''
# doc = "test\Projects-Topics.pdf"
# qr_code_path = './image/qrcode.png'
# signed_doc = "test\signed_qual.pdf"
# sign_a = a.signing_pdf(doc) # length =  666 bytes

# qr.generate_qr(sign_a, qr_code_path)
# qr.add_qr_code_to_pdf(doc, qr_code_path, signed_doc)


# test verify
# sign_doc = "test\signed_qual.pdf"
# qr.remove_qr_code_from_pdf(sign_doc, "test\\test.pdf")
# veri = a.verify(sign_a, './test/test.pdf')
# print(veri)
# h còn tạo cert thử với in mã qr vào document
