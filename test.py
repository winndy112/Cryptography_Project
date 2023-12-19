# from OpenSSL import *
# import OpenSSL

# def createKeyPair(type, bits):
#     """
#     Create a public/private key pair
#     Arguments: Type - Key Type, must be one of TYPE_RSA and TYPE_DSA
#                bits - Number of bits to use in the key (1024 or 2048 or 4096)
#     Returns: The public/private key pair in a PKey object
#     """
#     pkey = OpenSSL.crypto.PKey()
#     pkey.generate_key(type, bits)
#     return pkey

# def create_self_signed_cert(pKey):
#     """Create a self signed certificate. This certificate will not require to be signed by a Certificate Authority."""
#     # Create a self signed certificate
#     cert = OpenSSL.crypto.X509()
#     # Common Name (e.g. server FQDN or Your Name)
#     cert.get_subject().CN = "BASSEM MARJI"
#     # Serial Number
#     cert.set_serial_number(int(time.time() * 10))
#     # Not Before
#     cert.gmtime_adj_notBefore(0)  # Not before
#     # Not After (Expire after 10 years)
#     cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
#     # Identify issue
#     cert.set_issuer((cert.get_subject()))
#     cert.set_pubkey(pKey)
#     cert.sign(pKey, 'md5')  # or cert.sign(pKey, 'sha256')
#     return cert

# def load():
#     """Generate the certificate"""
#     summary = {}
#     summary['OpenSSL Version'] = OpenSSL.__version__
#     # Generating a Private Key...
#     key = createKeyPair(OpenSSL.crypto.TYPE_RSA, 1024)
#     # PEM encoded
#     with open('.\static\private_key.pem', 'wb') as pk:
#         pk_str = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
#         pk.write(pk_str)
#         summary['Private Key'] = pk_str
#     # Done - Generating a private key...
#     # Generating a self-signed client certification...
#     cert = create_self_signed_cert(pKey=key)
#     with open('.\static\certificate.cer', 'wb') as cer:
#         cer_str = OpenSSL.crypto.dump_certificate(
#             OpenSSL.crypto.FILETYPE_PEM, cert)
#         cer.write(cer_str)
#         summary['Self Signed Certificate'] = cer_str
#     # Done - Generating a self-signed client certification...
#     # Generating the public key...
#     with open('.\static\public_key.pem', 'wb') as pub_key:
#         pub_key_str = OpenSSL.crypto.dump_publickey(
#             OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())
#         #print("Public key = ",pub_key_str)
#         pub_key.write(pub_key_str)
#         summary['Public Key'] = pub_key_str
#     # Done - Generating the public key...
#     # Take a private key and a certificate and combine them into a PKCS12 file.
#     # Generating a container file of the private key and the certificate...
#     p12 = OpenSSL.crypto.PKCS12()
#     p12.set_privatekey(key)
#     p12.set_certificate(cert)
#     open('.\static\container.pfx', 'wb').write(p12.export())
#     # You may convert a PKSC12 file (.pfx) to a PEM format
#     # Done - Generating a container file of the private key and the certificate...
#     # To Display A Summary
#     print("## Initialization Summary ##################################################")
#     print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
#     print("############################################################################")
#     return True


# import fitz  # PyMuPDF

# def attach_image_to_pdf(pdf_path, image_path, output_pdf_path, x, y):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)

#     # Open the image file
#     image_document = fitz.open(image_path)

#     # Get the first page of the PDF document
#     pdf_page = pdf_document[0]

#     # Get the first page of the image document
#     image_page = image_document[0]

#     # Copy the image to the PDF page
#     pdf_page.insert_image((x, y), image_page)

#     # Save the modified PDF
#     pdf_document.save(output_pdf_path)
    
#     # Close the PDF and image documents
#     pdf_document.close()
#     image_document.close()

# # Example usage:
# input_file = "./test/Projects-Topics.pdf"
# qr_code_path = './image/qrcode.png'
# output_file = "./test/signed_Projects-Topics.pdf"
# x_position = 0  # Adjust the X position of the image
# y_position = 0  # Adjust the Y position of the image

# attach_image_to_pdf(input_file, qr_code_path, output_file, x_position, y_position)


# import PyPDF2
# pdf_file = "test/signed_qual.pdf"

# with open(pdf_file, 'rb') as file:
#     #signature = 'test'
#     # Create a PDF reader
#     pdf_reader = PyPDF2.PdfReader(file)
#     # Get the document information (metadata)
#     meta = pdf_reader.metadata
#     print(meta)
#     # pdf_writer = PyPDF2.PdfWriter()
#     # xmp_metadata = f"signature"
#     # pdf_writer.add_metadata({PyPDF2.generic.NameObject('/Signature'): xmp_metadata.encode()})
#     # with open('output.pdf', 'wb') as fout:
#     #             pdf_writer.write(fout)

