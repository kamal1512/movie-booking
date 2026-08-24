
def test_login(client, setup_test_data):
    response = client.post(
        "/users/login",
        data={
            "username": "ka@gmail.com",
            "password": "123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data.get("token_type") == "bearer"

def test_invalid_login(client, setup_test_data):

    response = client.post(
        "/users/login",
        data={
            "username": "alice",
            "password": "wrong-password"
        }
    )

    assert response.status_code == 401

def test_protected_endpoint(client, setup_test_data):

    login_response = client.post(
        "/users/login",
        data={
            "username": "ka@gmail.com",
            "password": "123"
        }
    )

    print("LOGIN STATUS:", login_response.status_code)
    print("LOGIN RESPONSE:", login_response.json())

    token = login_response.json()[
        "access_token"
    ]

    response = client.get(
        "/users/me",
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_protected_endpoint_without_token(client, setup_test_data):
        response = client.get(
            "/users/me"
        )

        assert response.status_code == 401