import pytest

from app.main import app
from app.db import engine, get_db
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


@pytest.fixture
def connect_to_engine():
    engine_connection = engine.connect()
    yield engine_connection
    engine_connection.close()


@pytest.fixture
def wrap_the_session(connect_to_engine):
    connect_to_engine.begin_nested()
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=connect_to_engine)
    wrapped_session = TestSession()
    yield wrapped_session
    wrapped_session.rollback()


@pytest.fixture
def client(wrap_the_session):
    app.dependency_overrides[get_db] = lambda: wrap_the_session
    yield TestClient(app)
    app.dependency_overrides.clear()