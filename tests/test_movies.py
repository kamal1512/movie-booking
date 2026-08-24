from fastapi.testclient import TestClient

from app.main import app

# client = TestClient(app)

def test_root(client):
    response = client.get("/")

    assert  response.status_code == 200

def test_get_movie(client, setup_test_data):
    user, movie = setup_test_data

    response = client.get(f"/movies/{movie.id}")

    assert response.status_code == 200

    data = response.json()

    assert data.get("id") == movie.id
