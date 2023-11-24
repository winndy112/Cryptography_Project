import OpenSSL

from PDFNetPython3.PDFNetPython import *


def attach_sig_to_pdf(input_file):
    PDFNet.Initialize()
    doc = PDFDoc(input_file)
