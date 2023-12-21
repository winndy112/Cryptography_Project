from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy_utils import database_exists, create_database

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12012004vert@localhost:3306/data_falcon"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Declarative Base
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


