# pip install qrcode
import qrcode

# hàm tạo QR dựa bao gồm signature và certificate

def generate_qr(data, output_file):
    qr = qrcode.QRCode(version=40)
    qr.add_data(data)
    qr.make()
    image = qr.make_image()
    image.save(output_file)
        