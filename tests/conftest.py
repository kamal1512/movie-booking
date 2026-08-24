import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.db.database import (
    SessionLocal
)
from app.core.dependencies import get_db

@pytest.fixture
def client():

    return TestClient(app)

@pytest.fixture
def db():

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()