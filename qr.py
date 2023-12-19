# pip install qrcode
import qrcode
import fitz
import cv2


'''
hàm tạo QR dựa bao gồm signature và certificate
'''

def generate_qr(data, output_file):
    qr = qrcode.QRCode(version=40)
    qr.add_data(data)
    qr.make()
    image_size = (370, 370)
    image = qr.make_image()
    resized_image = image.resize(image_size)
    resized_image.save(output_file)

'''
hàm gán mã QR vào văn bằng
'''

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
'''
Hàm xóa mã QR ra khỏi văn bằng trước khi tiến hành verify
'''

def remove_qr_code_from_pdf(pdf_path, output_file):
    # Open the PDF file
    document = fitz.open(pdf_path)
    
    # Get the first page of the PDF document
    page = document[0]

    # Remove all images from the page (you may need to adjust this logic based on your specific case)
    images = page.get_images(full=True)
    for img_index, img in enumerate(images):
        # nếu ảnh này là ảnh qr
        if img[2] == img[3] == 370:
            xref = img[0]
            page.delete_image(xref)
    # Save the modified PDF to the output file
    document.save(output_file)
    document.close()

