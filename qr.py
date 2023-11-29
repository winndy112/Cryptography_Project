# pip install qrcode
import qrcode
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image

# hàm tạo QR dựa bao gồm signature và certificate
def generate_qr(data, output_file):
    qr = qrcode.QRCode(version=40)
    qr.add_data(data)
    qr.make()
    image = qr.make_image()
    image.save(output_file)

def add_qr_code_to_pdf(qr_code_path, pdf_path, output_pdf_path):

    pdf_reader = PdfReader(pdf_path)  
    page = pdf_reader.pages[0]

    qr_code_img = Image.open(qr_code_path)
    resized_image = qr_code_img.resize((370, 370))
    resized_image.save(qr_code_path)
    img_width, img_height = qr_code_img.size
    
    page_width = page.mediabox[2]
    
    print(page.mediabox)
    x_position = int((page_width - img_width) / 2)
    # print(type(x_position))
    y_position = 0

    img_canvas = canvas.Canvas(output_pdf_path)
    img_canvas.drawImage(qr_code_path, x_position, y_position,  
                        width=img_width, height=img_height)
    img_canvas.save()

    with open(output_pdf_path, 'wb') as output_pdf_file:
        writer = PdfWriter()
        writer.add_page(page)
        writer.write(output_pdf_file)

# def scan_qr(inpurt_file):

if __name__ == "__main__":
    input_file = "./test/Projects-Topics.pdf"
    qr_code_path = './image/qrcode.png'
    output_file = "./test/signed_Projects-Topics.pdf"

    add_qr_code_to_pdf(qr_code_path, input_file, output_file)
