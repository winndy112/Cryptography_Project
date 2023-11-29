import digital_signature as dsa
import qr 


a = dsa.digital_signature()
a.create_key()

# save_bytes_to_pem(, 'output.pem', 'PUBLIC KEY')

# test sign
doc = "test\sample_qual.pdf"
qr_code_path = './image/qrcode.png'
signed_doc = "test\signed_qual.pdf"
sign_a = a.signing_pdf(doc)

qr.generate_qr(sign_a, qr_code_path)
qr.add_qr_code_to_pdf(doc, qr_code_path, signed_doc)


# test verify
sign_doc = "test\signed_qual.pdf"
qr.remove_qr_code_from_pdf(sign_doc, "test\\test.pdf")
veri = a.verify(sign_a, './test/test.pdf')
print(veri)
# h còn tạo cert thử với in mã qr vào document
