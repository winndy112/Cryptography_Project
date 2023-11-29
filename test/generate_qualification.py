from fpdf import FPDF # pip install fpdf
import random
import string

# characters= string.ascii_letters + string.digits

for i in range(150):
    # random_name = ''.join(random.choice(characters) for _ in range(20))
    path = f"file\\test_qualification.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 16)
    pdf.cell(40, 10, 'Lorem Ipsum')
    pdf.output(path, 'F')