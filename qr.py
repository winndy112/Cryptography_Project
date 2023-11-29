# pip install qrcode
import qrcode
import fitz


# hàm tạo QR dựa bao gồm signature và certificate
def generate_qr(data, output_file):
    qr = qrcode.QRCode(version=40)
    qr.add_data(data)
    qr.make()
    image_size = (370, 370)
    image = qr.make_image()
    resized_image = image.resize(image_size)
    resized_image.save(output_file)

def add_qr_code_to_pdf(pdf_path, image_file, output_file):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    # Get the first page of the PDF document
    
    pdf_page = pdf_document[0]
    page_size = pdf_page.mediabox
    image_rectangle = fitz.Rect(20, page_size.height - 120, 120, page_size.height - 20)
    # add the image
    pdf_page.insert_image(image_rectangle, filename=image_file)
    pdf_document.save(output_file)
    

def scan_qr(inpurt_file):

# def detach_qr(input_file):

if __name__ == "__main__":
    input_file = "./test/sample_qual.pdf"
    qr_code_path = './image/qrcode.png'
    output_file = "./test/signed.pdf"
    add_qr_code_to_pdf( input_file, qr_code_path, output_file)
