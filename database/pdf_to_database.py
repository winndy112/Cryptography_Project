import mysql.connector

#Lưu ý: phải tạo trước giá trị qrcode_id

def save_pdf_to_database(file_path, file_name, qrcode_id):
    # Kết nối tới cơ sở dữ liệu
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="DATA_FALCON"
    )
    
    # Mở tệp PDF và đọc dữ liệu
    with open('E:\ThnBih_HK3\MatMaHoc\project\code\meo.pdf', 'rb') as file:
        pdf_data = file.read()

    # Tạo câu truy vấn SQL để chèn dữ liệu vào bảng documents
    insert_query = "INSERT INTO documents (name, file, qrcode_id) VALUES (%s, %s, %s)"
    data = (file_name, pdf_data, qrcode_id)

    # Thực thi câu truy vấn
    cursor = db_connection.cursor()
    cursor.execute(insert_query, data)

    # Lưu thay đổi vào cơ sở dữ liệu
    db_connection.commit()

    # Đóng kết nối và con trỏ
    cursor.close()
    db_connection.close()

# Sử dụng hàm save_pdf_to_database để lưu tệp PDF vào cơ sở dữ liệu
file_path = 'E:\ThnBih_HK3\MatMaHoc\project\code\meo.pdf'  # Đường dẫn đến tệp PDF
file_name = 'test.pdf'  # Tên tệp PDF
qrcode_id = 1  # ID của mã QR tương ứng

save_pdf_to_database(file_path, file_name, qrcode_id)
