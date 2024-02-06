import json


def test_create_user(client):
    data = {"first_name":"test", "last_name":"user","email":"testuser@nofoobar.com","password":"testing"}
    response = client.post("/users/",json.dumps(data))
    assert response.status_code == 200 
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True
    assert response.json()["is_staff"] == False