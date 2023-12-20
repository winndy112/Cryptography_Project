import base64

# Đường dẫn đến tệp tin chứa public key
public_key_file = "public.txt"

# Đọc public key từ tệp tin
with open(public_key_file, "r") as file:
    public_key = file.read().strip()

# Tạo thông tin chứng chỉ
username = "Nguyễn Hoàng Tú Anh"
address = "UIT"

# Tạo nội dung tệp cer
cert_content = f"Username: {username}\nAddress: {address}\nPublic Key: {public_key}"

# Chuyển đổi nội dung cert thành base64
cert_base64 = base64.b64encode(cert_content.encode("utf-8"))

# Lưu tệp cer
with open("certificate.cer", "wb") as cert_file:
    cert_file.write(cert_base64)
