from database import Base
from sqlalchemy import Column, Integer, String, Date, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

class Students(Base):
    __tablename__= "StudentInfor"
    id_sv = Column(Integer, primary_key=True, index=True)
    school = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String) # the request will be rehashing password
    
class Ins(Base):
    __tablename__ =  'Institution' 
    institution_id = Column(Integer, primary_key= True, index= True)
    institution_name = Column(String)
    authority_person = Column(String, unique= True)
    certificate_file = Column(LargeBinary)

class Quals(Base):
    __tablename__= 'Qualifications'
    degree_code = Column(Integer, primary_key=True, index=True)
    id_sv = Column(Integer, ForeignKey("StudentInfor.id_sv"))
    issue_date = Column(Date)
    expiration_date = Column(Date)
    pdf_file = Column(LargeBinary)
    institution_id = Column(Integer, ForeignKey("Institution.institution_id"))
    
