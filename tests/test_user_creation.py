import pytest
import allure

from data import ResponseMessages
from helpers import generate_user_data, user_creation, user_get_access_token
from generators import email_generator, password_generator, name_generator

class TestUserCreation:

    @allure.title("Пользователь успешно создан при передаче в ручку всех обязательных полей")
    def test_user_created_successfully(self, delete_user_after_test):
        user_data = generate_user_data()
        response_create = user_creation(user_data)
        assert response_create.status_code == 200
        assert response_create.json()["success"] is True
        access_token = response_create.json()["accessToken"]
        assert access_token is not None
        delete_user_after_test.append(access_token)

    @allure.title("Ошибка при создании пользователя, который уже ранее создан")
    def test_create_duplicate_user_shows_error(self, delete_user_after_test):
        user_data = generate_user_data()
        response_user = user_creation(user_data)
        assert response_user.status_code == 200
        access_token = response_user.json()["accessToken"]
        response_duplicate_user = user_creation(user_data)
        assert response_duplicate_user.status_code == 403 
        assert response_duplicate_user.json()["success"] is False
        assert response_duplicate_user.json()["message"] == ResponseMessages.DUPLICATE_USER
        delete_user_after_test.append(access_token)

    @allure.title("Ошибка при создании пользователя при передаче в ручку не всех обязательных полей")
    @pytest.mark.parametrize(
        "user_payload, missing_field_name", 
        [
            ({"password": password_generator(), "name": name_generator()}, "email"),
            ({"email": email_generator(), "name": name_generator()}, "password"),
            ({"email": email_generator(), "password": password_generator()}, "name")
        ]
        )
    def test_create_user_without_required_field_shows_error(self, user_payload, missing_field_name):
        response = user_creation(user_payload)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == ResponseMessages.ERROR_CREATE_WITHOUT_REQUIRED_FIELD
