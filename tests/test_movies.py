from fastapi.testclient import TestClient

from app.main import app

# client = TestClient(app)

def test_root(client):
    response = client.get("/")

    assert  response.status_code == 200

def test_get_movie(client):

    response = client.get("/movies/1")

    assert response.status_code == 200

    data = response.json()

    assert data.get("id") == 1
