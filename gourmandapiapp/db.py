from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from gourmandapiapp.config import settings
import redis
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.pg_oltp_api_user}:{settings.pg_oltp_api_password}@{settings.pg_oltp_api_host}/{settings.pg_oltp_api_db}"
if os.environ.get("GOURMAND_ENV") == 'staging':
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.pg_oltp_api_user}:{settings.pg_oltp_api_password}@{settings.pg_oltp_api_host}/{settings.pg_oltp_api_db_test}"
    logging.info(msg=f'Entering {os.environ.get("ENV")} env')

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def start_redis():
    redis_client = redis.Redis(
        host='redis',
        port=6379, db=10)
    try:
        yield redis_client
    finally:
        None