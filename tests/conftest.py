import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command

from app.main import app
from app.api.deps import get_db
from app.core.config import settings

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", settings.TEST_DATABASE_URL)
    command.upgrade(config, "head")
    yield

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db_session(apply_migrations):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]