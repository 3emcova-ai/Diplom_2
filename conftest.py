import pytest

from helpers import user_delete, generate_user_data, user_creation, get_ingredients


@pytest.fixture
def delete_user_after_test():
    user_tokens = []
    yield user_tokens
    for access_token in user_tokens:
        if access_token:
            user_delete(access_token)

@pytest.fixture
def create_registred_delete_user():
    user_data = generate_user_data()
    response = user_creation(user_data)
    assert response.status_code == 200, f"Ошибка создания пользователя: {response.text}"
    access_token = response.json()["accessToken"]
    assert access_token is not None, "Токен не получен от сервера"
    yield {"data": user_data, "token": access_token}
    user_delete(access_token)

@pytest.fixture
def return_ingredients():
    response = get_ingredients()
    assert response.status_code == 200
    data = response.json()["data"]
    return [data[0]["_id"], data[1]["_id"]]
