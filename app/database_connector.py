from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
from .config import settings

def getconn():
    with Connector() as connector:
        conn = connector.connect(
            settings.database_hostname,  
            "pg8000",
            user=settings.database_username,
            password=settings.database_password,
            db=settings.database_name,
            ip_type=IPTypes.PUBLIC,  
        )
    return conn


SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"

engine = create_engine(SQLALCHEMY_DATABASE_URL, creator=getconn)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
