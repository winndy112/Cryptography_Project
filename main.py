import digital_signature as dsa
import qr 


a = dsa.digital_signature()
a.create_key()

# save_bytes_to_pem(, 'output.pem', 'PUBLIC KEY')


input_file = "./test/Projects-Topics.pdf"
qr_code_path = './image/qrcode.png'
output_file = "./test/signed_Projects-Topics.pdf"
sign_a = a.signing_pdf(input_file)
qr.generate_qr(sign_a, qr_code_path)
qr.add_qr_code_to_pdf(qr_code_path, input_file, output_file)

# veri = a.verify(sign_a, input_file)
# print(veri)
# h còn tạo cert thử với in mã qr vào document
