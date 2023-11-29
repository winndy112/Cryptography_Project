import mysql.connector

def retrieve_pdf_from_database(document_id, output_path):
    # Kết nối tới cơ sở dữ liệu
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="DATA_FALCON"
    )
    
    # Tạo câu truy vấn SQL để truy xuất dữ liệu từ bảng documents
    select_query = "SELECT file FROM documents WHERE id = %s"
    data = (document_id,)

    # Thực thi câu truy vấn
    cursor = db_connection.cursor()
    cursor.execute(select_query, data)

    # Truy xuất dữ liệu từ kết quả truy vấn
    result = cursor.fetchone()

    if result is not None:
        # Lưu dữ liệu PDF thành tệp mới
        pdf_data = result[0]
        with open(output_path, 'wb') as file:
            file.write(pdf_data)

        print(f"Đã lưu tệp PDF tại: {output_path}")
    else:
        print("Không tìm thấy tệp PDF trong cơ sở dữ liệu.")

    # Đóng kết nối và con trỏ
    cursor.close()
    db_connection.close()

# Sử dụng hàm retrieve_pdf_from_database để truy xuất và lưu tệp PDF từ cơ sở dữ liệu
document_id = 2  # ID của tệp PDF muốn truy xuất
output_path = 'E:\ThnBih_HK3\MatMaHoc\project\code\lay_pdf_ra.pdf'  # Đường dẫn đến tệp PDF đầu ra

retrieve_pdf_from_database(document_id, output_path)
