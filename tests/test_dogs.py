from tests.test_users import login_app, login
import json

dog_prefix = "/api/dogs/"
dog_info = {
    "name": "kyrantinia",
    "picture": "https://images.dog.ceo/breeds/cattledog-australian/IMG_3056.jpg",
    "is_adopted": True,
    "created_date": "2021-04-05T22:07:41.298970",
    "publisher": {
        "name": "camilo",
        "email": "camilo@gmail.com"
    },
    "adopter": {
        "name": "daniel",
        "email": "daniel@gmail.com"
    }
}
update_dog = {
    "is_adopted": True,
    "adopter_id": 3
}


def test_get_all_dogs(test_app):
    response = test_app.get(dog_prefix)
    assert response.status_code == 200
    response = response.json()
    assert response['total'] == 3
    assert len(response['dogs']) == 3
    assert response['dogs'][0]['name'] == "firulais"


def test_adopted_dogs(test_app):
    response = test_app.get(f"{dog_prefix}adopted")
    assert response.status_code == 200
    response = response.json()
    assert response['total'] == 1
    assert len(response['dogs']) == 1
    assert response['dogs'][0]['name'] == "kyrantinia"
    assert response['dogs'][0]['is_adopted'] == True


def test_find_dog_by_name(test_app):
    response = test_app.get(f"{dog_prefix}kyrantinia")
    assert response.status_code == 200
    response = response.json()
    assert response == dog_info


def test_not_dog_find(test_app):
    response = test_app.get(f"{dog_prefix}someotherdogname")
    assert response.status_code == 404


def test_delete_dog(test_app):
    response = login_app(test_app, login)
    assert response.status_code == 200
    token = response.json()
    headers = {"accept": "application/json",
               "Authorization": f"Bearer {token['access_token']}"}
    response = test_app.delete(f"{dog_prefix}milutata", headers=headers)
    assert response.status_code == 204
    response = test_app.get(dog_prefix)
    assert response.status_code == 200
    response = response.json()
    assert response['total'] == 2
    assert len(response['dogs']) == 2


def test_create_dog(test_app):
    response = login_app(test_app, login)
    assert response.status_code == 200
    token = response.json()
    headers = {"accept": "application/json",
               "Authorization": f"Bearer {token['access_token']}"}
    response = test_app.post(f"{dog_prefix}clifford", headers=headers)
    assert response.status_code == 200


def test_create_repeat_dog(test_app):
    response = login_app(test_app, login)
    assert response.status_code == 200
    token = response.json()
    headers = {"accept": "application/json",
               "Authorization": f"Bearer {token['access_token']}"}
    response = test_app.post(f"{dog_prefix}kyrantinia", headers=headers)
    assert response.status_code == 409
    response = response.json()
    assert response['detail'] == "There is already a dog with this name"


def test_update_dog(test_app):
    response = login_app(test_app, login)
    assert response.status_code == 200
    token = response.json()
    headers = {"accept": "application/json",
               "Authorization": f"Bearer {token['access_token']}"}
    response = test_app.put(f"{dog_prefix}milutata", headers=headers, data=json.dumps(update_dog))
    assert response.status_code == 200
    response = response.json()
    assert response['is_adopted'] == True
    assert response['adopter']['name'] == "paola"


def test_not_update_dog(test_app):
    response = test_app.put(f"{dog_prefix}milutata")
    assert response.status_code == 401
    response = response.json()
    assert response['detail'] == "Not authenticated"
