import pytest

from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.main import app
from app.db.database import (
    SessionLocal
)
from app.core.dependencies import get_db
from app.models.movie import Movie
from app.models.user import User


@pytest.fixture
def client():

    return TestClient(app)

@pytest.fixture
def setup_test_data(db):
    user = User(
        email="ka@gmail.com",
        username="ka@gmail.com",
        hashed_password=hash_password("123"),
        is_active=True
    )

    movie = Movie(
        name="Test Movie",
        language="English",
        duration=120
    )

    db.add(user)
    db.add(movie)
    db.commit()
    db.refresh(user)
    db.refresh(movie)

    yield user, movie

    db.delete(movie)
    db.delete(user)
    db.commit()

@pytest.fixture
def db():

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()