import mysql.connector
from PIL import Image
from io import BytesIO

# Kết nối tới cơ sở dữ liệu MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="test_img"
)

# Thực hiện câu lệnh SELECT để truy xuất hình ảnh từ cơ sở dữ liệu
sql = "SELECT data FROM images WHERE name = %s"
val = ("qrcode.png",)
cursor = mydb.cursor()
cursor.execute(sql, val)
result = cursor.fetchone()

# Hiển thị hình ảnh từ dữ liệu nhận được
image_data = result[0]
image = Image.open(BytesIO(image_data))
image.show()