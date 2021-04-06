import json

user_prefix = "/api/user/"
new_user = {
    "name": "string",
    "email": "awaw@example.com",
    "password": "string"
}
repeat_user = {
    "name": "paola",
    "email": "paola@gmail.com",
    "password": "string"
}

login = {
    "username": "daniel@gmail.com",
    "password": "string"
}
update_user = {
    "name": "othername",
    "email": "julio@gmail.com"
}
bad_update_user = {
    "name": "othername",
    "email": "paolas@gmail.com"
}


def test_create_user(test_app):
    response = test_app.post(user_prefix, data=json.dumps(new_user))
    assert response.status_code == 200
    response = response.json()
    assert response["name"] == new_user["name"]
    assert response["email"] == new_user["email"]


def test_create_two_same_user(test_app):
    response = test_app.post(user_prefix, data=json.dumps(repeat_user))
    assert response.status_code == 409
    response = response.json()
    assert response["detail"] == "There is already a user with this email"


def test_login(test_app):
    response = login_app(test_app, login)
    assert response.status_code == 200
    response = response.json()
    assert response['token_type'] == "bearer"


def test_bad_login(test_app):
    bad_login = login.copy()
    bad_login['password'] = "other password"
    response = login_app(test_app, bad_login)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == "Incorrect email or password"


def test_user_info(test_app):
    response = login_app(test_app, login)
    assert response.status_code == 200
    token = response.json()
    headers = {"accept": "application/json",
               "Authorization": f"Bearer {token['access_token']}"}
    response = test_app.get(user_prefix + "info", headers=headers)
    assert response.status_code == 200
    response = response.json()
    assert response['email'] == login['username']


def test_user_update_state(test_app):
    response = login_app(test_app, login)
    assert response.status_code == 200
    token = response.json()
    headers = {"accept": "application/json",
               "Authorization": f"Bearer {token['access_token']}"}
    response = test_app.put(user_prefix + "state", headers=headers)
    assert response.status_code == 200
    response = login_app(test_app, login)
    assert response.status_code == 400


def test_user_update(test_app):
    response = login_app(test_app, login)
    assert response.status_code == 200
    token = response.json()
    headers = {"accept": "application/json",
               "Authorization": f"Bearer {token['access_token']}"}
    response = test_app.put(user_prefix, headers=headers, data=json.dumps(update_user))
    assert response.status_code == 200
    response = response.json()
    assert response['name'] == update_user['name']
    assert response['email'] == update_user['email']
    response = login_app(test_app, login)
    assert response.status_code == 400


def login_app(test_app, data):
    return test_app.post(user_prefix + "login", data=data)
