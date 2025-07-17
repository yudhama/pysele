import requests

def test_create_user():
    url = "https://petstore.swagger.io/v2/user"
    payload = {
        "id": 12345,
        "username": "apitestuser",
        "firstName": "API",
        "lastName": "Tester",
        "email": "apitestuser@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    assert response.json()["message"] == str(payload["id"])

if __name__ == "__main__":
    test_create_user()