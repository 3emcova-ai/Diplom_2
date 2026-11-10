import allure
import generators

from data import ResponseMessages
from helpers import user_login


class TestUserLogin:

    @allure.title("Ранее зарегистрированный пользователь успешно авторизован")
    def test_user_login_successfully(self, create_registred_delete_user):
        user_data = create_registred_delete_user["data"]
        access_token = create_registred_delete_user["token"]
        response_login = user_login(user_data['email'], user_data['password'])
        assert response_login.status_code == 200
        assert response_login.json()["success"] is True
        assert response_login.json()["accessToken"] is not None
        
    @allure.title("Ошибка авторизации пользователя с неверным email")
    def test_login_with_incorrect_email_shows_error(self, create_registred_delete_user):
        user_data = create_registred_delete_user["data"]
        access_token = create_registred_delete_user["token"]
        response_login = user_login(generators.email_generator(), user_data['password'])
        assert response_login.status_code == 401
        assert response_login.json()["success"] is False
        assert response_login.json()["message"] == ResponseMessages.ERROR_INCORRECT_LOGIN_PASSWORD
        
    @allure.title("Ошибка авторизации пользователя с неверным паролем")
    def test_login_with_incorrect_password_shows_error(self, create_registred_delete_user):
        user_data = create_registred_delete_user["data"]
        access_token = create_registred_delete_user["token"]
        response_login = user_login(user_data['email'], generators.password_generator())
        assert response_login.status_code == 401
        assert response_login.json()["success"] is False
        assert response_login.json()["message"] == ResponseMessages.ERROR_INCORRECT_LOGIN_PASSWORD
       