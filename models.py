from database import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String, Date, LargeBinary, ForeignKey

class Ins(Base):
    __tablename__ =  'Institution' 
    institution_id = Column(Integer, primary_key= True, index= True)
    institution_name = Column(String)
    authority_person = Column(String)
    email_address = Column(String, unique = True)
    hashed_password = Column(String)
    certificate_file = Column(LargeBinary)

class Students(Base):
    __tablename__= "StudentInfor"
    id_sv = Column(Integer, primary_key=True, index=True)
    school = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    
class Quals(Base):
    __tablename__= 'Qualifications'
    degree_code = Column(Integer, primary_key=True, index=True)
    id_sv = Column(Integer, ForeignKey("StudentInfor.id_sv"))
    issue_date = Column(Date)
    expiration_date = Column(Date)
    institution_id = Column(Integer, ForeignKey("Institution.institution_id"))   
    pdf_file = Column(LargeBinary)



'''
Testing
'''
# db = SessionLocal()
# with open(r"test\signed_qual.pdf", "rb") as f:
#     data = f.read()
# with open(r"cert.pem", "rb") as f:
#     cert = f.read()
# # Thêm dữ liệu mẫu
# # new_institution = Ins(institution_id= 1, institution_name="Example University", authority_person="Admin", email_address="admin@example.com", hashed_password="hashed_password", certificate_file=cert)
# # db.add(new_institution)
# # db.commit()

# new_student = Students(id_sv = 5, school="School of Engineering", first_name="Anh", last_name="Quynh")
# db.add(new_student)
# db.commit()
# new_qualification = Quals(degree_code = 10, id_sv = 5, issue_date="2022-01-01", expiration_date="2025-01-01", pdf_file=data, institution_id=1)
# db.add(new_qualification)
# db.commit()

# # Đóng session
# db.close()

