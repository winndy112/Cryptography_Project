# pip install qrcode

import qrcode

# String data want to encode into a QR code
data = "abc"

# Create a QR code instance with version 40
qr = qrcode.QRCode(version=40)

# Add data to the QR code
qr.add_data(data)

# Generate the QR code as an image
qr.make()

# Get the image as a PIL Image object
image = qr.make_image()

# Save the image to a file
image.save("qrcode.png")
