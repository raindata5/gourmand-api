from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from gourmandapiapp.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.pg_oltp_api_user}:{settings.pg_oltp_api_password}:{settings.pg_oltp_api_port}@{settings.pg_oltp_api_host}/{settings.pg_oltp_api_db}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()