from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image

def add_qr_code_to_pdf(qr_code_path, pdf_path, output_pdf_path):

    pdf_reader = PdfReader(pdf_path)  
    page = pdf_reader.pages[0]

    qr_code_img = Image.open(qr_code_path)

    img_width = 1850
    img_height = 1850  

    page_width = page.mediabox[2]

    x_position = (page_width - img_width) / 2
    y_position = 0

    img_canvas = canvas.Canvas(output_pdf_path)
    img_canvas.drawImage(qr_code_path, x_position, y_position,  
                        width=img_width, height=img_height)

    with open(output_pdf_path, 'wb') as output_pdf_file:
        writer = PdfWriter()
        writer.add_page(page)
        writer.write(output_pdf_file)

if __name__ == "__main__":
    qr_code_path = "E:/ThnBih_HK3/MatMaHoc/project/code/qrcode.png"
    pdf_path = "E:/ThnBih_HK3/MatMaHoc/project/code/test.pdf"
    output_pdf_path = "E:/ThnBih_HK3/MatMaHoc/project/code/test_with_qr.pdf"

    add_qr_code_to_pdf(qr_code_path, pdf_path, output_pdf_path)
