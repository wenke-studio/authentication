import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.core.database import Base
from server.dependencies import get_db
from server.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True, scope="session")
def global_context():
    # setup: override the get_db dependency for testing
    app.dependency_overrides[get_db] = override_get_db

    yield

    # teardown: drop the database
    file_location = engine.url.database
    engine.dispose()
    os.remove(file_location)


@pytest.fixture(autouse=True, scope="function")
def db_context():
    # setup: create tables
    Base.metadata.create_all(bind=engine)

    yield

    # teardown: drop tables
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def http():
    # create a new http client for each test
    yield TestClient(app)
