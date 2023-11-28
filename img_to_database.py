import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="test_img"
)

# Đọc dữ liệu của hình ảnh từ file PNG
with open("E:\ThnBih_HK3\MatMaHoc\project\code\qrcode.png", "rb") as file:
    image_data = file.read()

# Thực hiện câu lệnh INSERT để lưu trữ hình ảnh vào cơ sở dữ liệu
sql = "INSERT INTO images (name, data) VALUES (%s, %s)"
val = ("qrcode.png", image_data)
cursor = mydb.cursor()
cursor.execute(sql, val)
mydb.commit()