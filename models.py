from database import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String, Date, LargeBinary, ForeignKey

class Ins(Base):
    __tablename__ =  'Institution' 
    institution_id = Column(Integer, primary_key= True, index= True)
    institution_name = Column(String,  unique = True)
    authority_person = Column(String)
    email_address = Column(String, unique = True)
    public_file = Column(String)
    certificate_file = Column(LargeBinary)

class Students(Base):
    __tablename__= "StudentInfor"
    id_sv = Column(Integer, primary_key=True, index=True)
    school = Column(String)
    student_name = Column(String)

    
class Quals(Base):
    __tablename__= 'Qualifications'
    degree_code = Column(Integer, primary_key=True, index=True)
    id_sv = Column(Integer, ForeignKey("StudentInfor.id_sv"))
    issue_date = Column(Date)
    expiration_date = Column(Date)
    institution_id = Column(Integer, ForeignKey("Institution.institution_id"))   
    pdf_file = Column(LargeBinary)

