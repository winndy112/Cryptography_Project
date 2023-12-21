import base64

# Đường dẫn đến tệp tin chứa public key
public_key_file = "public.pem"

# Đọc public key từ tệp tin
with open(public_key_file, "r") as file:
    public_key = file.read().replace("-- Begin Falcon Public Key --", "").replace("-- End Falcon Public Key --", "").strip()
    #public_key = file.read().strip()

# Tạo thông tin chứng chỉ dưới dạng dictionary
certificate_info = {
    "Subject": "Chữ Kí ABC",
    "Author": "Nguyễn Hoàng Tú Anh",
    "Address": "UIT",
    "Public Key": public_key,
    "Serial Number": "123456",
    "Valid Dates": "2023-01-01 to 2023-12-31",
    "Additional Info 1": "Some additional information",
    "Additional Info 2": "More details",
}

# Tạo nội dung tệp cer
cert_content = "\n".join([f"{key}: {value}" for key, value in certificate_info.items()])

# Chuyển đổi nội dung cert thành base64
cert_base64 = base64.b64encode(cert_content.encode("utf-8"))

begin = b"---BEGIN CERTIFICATE---\n"
end = b"\n---END CERTIFICATE---\n"

# Lưu tệp cer
with open("certificate.cer", "wb") as cert_file:
    cert_file.write(begin)
    cert_file.write(cert_base64)
    cert_file.write(end)
