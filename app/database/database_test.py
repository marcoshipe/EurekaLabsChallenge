import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.setup_teardown import setup_db, drop_db
from app.database.database import get_db
from app.config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.postgres_user}:{settings.postgres_password}@' \
                          f'db_test/{settings.postgres_db}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    setup_db(engine)
    yield
    drop_db(engine)


app.dependency_overrides[get_db] = override_get_db
