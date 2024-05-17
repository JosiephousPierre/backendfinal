from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://thisisclinic:thisispassword@159.65.128.24:3306/uic_clinic"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/uic_clinic" #Ito po yung ginamit kong URL for DB - Jem Pillora

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()