import allure
import generators

from data import ResponseMessages
from helpers import generate_user_data, user_creation, user_login


class TestUserLogin:

    @allure.title("Ранее зарегистрированный пользователь успешно авторизован")
    def test_user_login_successfully(self, delete_user_after_test):
        user_data = generate_user_data()
        response_create = user_creation(user_data)
        assert response_create.status_code == 200
        access_token = response_create.json()["accessToken"]
        response_login = user_login(user_data['email'], user_data['password'])
        assert response_login.status_code == 200
        assert response_login.json()["success"] is True
        assert response_login.json()["accessToken"] is not None
        delete_user_after_test.append(access_token)

    @allure.title("Ошибка авторизации пользователя с неверным email")
    def test_login_with_incorrect_email_shows_error(self, delete_user_after_test):
        user_data = generate_user_data()
        response_create = user_creation(user_data)
        response_login = user_login(generators.email_generator(), user_data['password'])
        assert response_login.status_code == 401
        assert response_login.json()["success"] is False
        assert response_login.json()["message"] == ResponseMessages.ERROR_INCORRECT_LOGIN_PASSWORD
        delete_user_after_test.append(response_create.json()["accessToken"])

    @allure.title("Ошибка авторизации пользователя с неверным паролем")
    def test_login_with_incorrect_password_shows_error(self, delete_user_after_test):
        user_data = generate_user_data()
        response_create = user_creation(user_data)
        response_login = user_login(user_data['email'], generators.password_generator())
        assert response_login.status_code == 401
        assert response_login.json()["success"] is False
        assert response_login.json()["message"] == ResponseMessages.ERROR_INCORRECT_LOGIN_PASSWORD
        delete_user_after_test.append(response_create.json()["accessToken"])
