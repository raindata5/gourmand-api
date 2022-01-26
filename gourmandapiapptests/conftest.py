from fastapi.testclient import TestClient
from gourmandapiapp.main import app
import pytest
from gourmandapiapp.db import get_db, start_redis
from gourmandapiapp.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command
import redis
from gourmandapiapp import models, schemas
import psycopg2


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.pg_oltp_api_user}:{settings.pg_oltp_api_password}@{settings.pg_oltp_api_host}/{settings.pg_oltp_api_db_test}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal_test_db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_session_db():
    # alembic_cfg = Config("/mnt/c/Users/Ron/git-repos/gourmandapi/alembic2.ini")
    # alembic_cfg.set_main_option('script_location', "/mnt/c/Users/Ron/git-repos/gourmandapi/g_test_db")
    # alembic_cfg.set_main_option("sqlalchemy.url", f"postgresql://{settings.pg_oltp_api_user}:{settings.pg_oltp_api_password}@{settings.pg_oltp_api_host}/{settings.pg_oltp_api_db_test}")
    print('ressetting test db now')
    # command.downgrade(alembic_cfg, "base")
    # command.upgrade(alembic_cfg, "head")
    # seems a bit faster and better to just truncate the tables
    ps_conn = psycopg2.connect(dbname=settings.pg_oltp_api_db_test, user=settings.pg_oltp_api_user, password=settings.pg_oltp_api_password, host= settings.pg_oltp_api_host, port=settings.pg_oltp_api_port)
    ps_cursor = ps_conn.cursor()
    sql_file = open('postgres-table-truncates.sql','r')
    ps_cursor.execute(sql_file.read())
    ps_conn.commit()
    ps_cursor.close()
    ps_conn.close()
    r1_client = redis.Redis(
        host='redis',
        port=6379, db=11)
    for key in r1_client.scan_iter("*"):
        r1_client.delete(key)
    test_db = SessionLocal_test_db()
    try:
        yield test_db
    finally:
        test_db.close()


@pytest.fixture
def test_client(test_session_db):
    def override_start_redis():
        r1_client = redis.Redis(
        host='redis',
        port=6379, db=11)
        try:
            yield r1_client
        finally:
            None
    def override_get_db():
        try:
            yield test_session_db
        finally:
            test_session_db.close()
    app.dependency_overrides[start_redis] = override_start_redis
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture
def inserted_business(test_session_db):
    # until models are created  I will just manually insert this data for tests
    ps_conn = psycopg2.connect(dbname=settings.pg_oltp_api_db_test, user=settings.pg_oltp_api_user, password=settings.pg_oltp_api_password, host= settings.pg_oltp_api_host, port=settings.pg_oltp_api_port)
    ps_cursor = ps_conn.cursor()
    sql_file = open('postgres_insert_for_tests.sql','r')
    ps_cursor.execute(sql_file.read())
    ps_conn.commit()
    ps_cursor.close()
    ps_conn.close()
    business = {"businessname":"1-chinese-restaurant-coinjock","chainname":"1 Chinese Restaurant",
    "addressline1":"US 158 Hwy Grandy Sh","addressline2":"None","addressline3":"None","latitude":"36.333440",
    "longitude":"-75.946890","zipcode":"27923","businessphone":"(252) 453-9712",
    "businessurl":"https://www.yelp.com/biz/1-chinese-restaurant-coinjock?adjust_creative=2FlPnf5brM1FB2UTY6vGnQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=2FlPnf5brM1FB2UTY6vGnQ",
    "is_closed":False,"distancetocounty":"8771","cityid":"1","countyid":"1","stateid":"1","paymentlevelid":"1"}
    bus_model = models.BusinessModelORM(**business)
    test_session_db.add(bus_model)
    test_session_db.commit()
    test_session_db.refresh(bus_model)
    
    return bus_model
