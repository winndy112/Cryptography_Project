from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# MySQL connection string
# Replace 'username', 'password', 'hostname', 'port', and 'database_name' with your MySQL credentials
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@hostname:port/database_name"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
