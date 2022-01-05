from fastapi import FastAPI
from fastapi.testclient import TestClient
from gourmandapiapp.main import app
import pytest
from gourmandapiapp.db import get_db

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.postgres_redis}-test"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

# SessionLocal_test_db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_session():
    sess = get_db()
    yield sess


@pytest.fixture
def test_client():
    # will override a bit later
    # def override_get_db():
    #     try:
    #         # db = TestingSessionLocal()

    #         yield db
    #     finally:
    #         db.close()
    yield TestClient(app)






