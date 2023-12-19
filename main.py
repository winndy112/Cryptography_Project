import digital_signature as dsa
import qr 
# thư viện chuyển đối tượng thành bytes
import pickle
import PyPDF2
# '''
# Tạo secret key và public key cho 
# '''

a = dsa.digital_signature()
a.load_public_key("Root_CA\\public.pem")
a.load_private_key("Root_CA\\private.pem")
# # print(a.sk)
# # print(a.pk)

# '''
# test sign và add vào qr
# '''

# doc = "test/test.pdf"
# qr_code_path = './image/qrcode.png'
# signed_doc = "test/signed_qual.pdf"
# a.signing_pdf(doc) # length =  666 bytes
# a.add_signature_to_metadata(doc, signed_doc)
# qr.generateQr_and_add_to_pdf(a.signature, signed_doc, qr_code_path)


# '''
# test verify
# '''

sign_doc = "test\signed_qual.pdf"
qr.remove_qr_code_from_pdf(sign_doc, "test\\verify_doc.pdf")
a.dettach_signature(sign_doc)
veri = a.verify("test\Projects-Topics.pdf")
print(veri)
# h còn tạo cert thử với in mã qr vào document
