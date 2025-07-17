import requests

def test_get_user():
    username = "apitestuser"  # Use the username you created previously
    url = f"https://petstore.swagger.io/v2/user/{username}"

    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    assert response.json()["username"] == username

if __name__ == "__main__":
    test_get_user()