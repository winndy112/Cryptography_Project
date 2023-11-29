import mysql.connector

def save_student_record():
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='DATA_FALCON'
    )
    cursor = cnx.cursor()

    insert_student_query = """
    INSERT INTO StudentInfor (id_sv, school, degree_code)
    VALUES (%s, %s, %s)
    """
    student_data = (1802, 'Sample School', '1')
    cursor.execute(insert_student_query, student_data)

    cnx.commit()
    cursor.close()
    cnx.close()

# Function to save a record to the Qualifications table
def save_record():
    # Establish a connection to the MySQL server
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='DATA_FALCON'
    )

    # Create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # Prepare the INSERT statement
    insert_query = """
    INSERT INTO Qualifications (degree_code, id_sv, issue_date, expiration_date, issuing_authority, pdf_file)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    # Set the values for the record to be inserted
    degree_code = '1'
    id_sv = 1802
    issue_date = '2012-01-01'
    expiration_date = '2022-01-01'
    issuing_authority = 'ABC'
    pdf_file_path = 'path_to_pdf_file.pdf'  # Replace with the actual file path

    # Read the PDF file and convert it to binary data
    with open('E:\ThnBih_HK3\MatMaHoc\project\code\meo.pdf', 'rb') as file:
        pdf_file_data = file.read()

    record_data = (degree_code, id_sv, issue_date, expiration_date, issuing_authority, pdf_file_data)

    # Execute the INSERT statement
    cursor.execute(insert_query, record_data)

    # Commit the changes to the database
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

# Function to retrieve the PDF file based on its file path
def retrieve_pdf():
    # Establish a connection to the MySQL server
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='DATA_FALCON'
    )

    # Create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # Retrieve the PDF file path from the database
    select_query = "SELECT pdf_file FROM Qualifications WHERE pdf_file_path = %s"
    pdf_file_path = 'E:\\ThnBih_HK3\\MatMaHoc\\project\\code\\lay_pdf_ra.pdf'

    # Execute the SELECT query
    cursor.execute(select_query, (pdf_file_path,))

    # Fetch the result
    result = cursor.fetchone()

    if result:
        # Extract the binary data of the PDF file
        pdf_file_data = result[0]

        # Save the PDF file to disk
        with open('path_to_save_pdf.pdf', 'wb') as file:
            file.write(pdf_file_data)
            print("PDF file retrieved and saved successfully.")
    else:
        print("PDF file not found in the database.")

    # Close the cursor and connection
    cursor.close()
    cnx.close()

# Main program
if __name__ == "__main__":
    while True:
        print("Chọn đi:")
        print("1. Lưu trước 1 StudentInfor để demo")
        print("2. Lưu thông in vào Qualifications")
        print("3. Truy xuất PDF")
        print("0. Exit")
        option = input("Option?: ")

        if option == '1':
            save_student_record()
            print("Ghi xong.")
        elif option == '2':
            save_record()
            print("Ghi xong.")
        elif option == '3':
            retrieve_pdf()
            print("Truy xuất xong.")
        elif option == '0':
            break
        else:
            print("Invalid option. Please try again.")
