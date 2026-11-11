import requests
import allure
import generators

from data import Urls

@allure.step('Гененирую Почту, Пароль и Имя для регистрации нового пользователя')
def generate_user_data():
    user_data = {
        'email': generators.email_generator(),
        'password': generators.password_generator(),
        'name': generators.name_generator()
    }
    return user_data

@allure.step('Регистрирую пользователя')
def user_creation(user_data):
    return requests.post(f'{Urls.STELLAR_BURGERS_URL}{Urls.CREATE_USER}', json=user_data)

@allure.step('Осуществляю авторизацию пользователя')
def user_login(email, password):
    return requests.post(f'{Urls.STELLAR_BURGERS_URL}{Urls.LOGIN_USER}', json={
    'email': email,
    'password': password
    })

@allure.step('Удаляю пользователя')
def user_delete(access_token):
    headers = {"Authorization": access_token}
    return requests.delete(f'{Urls.STELLAR_BURGERS_URL}{Urls.DELETE_USER}', headers=headers)

@allure.step('Получаю данные об ингредиентах')
def get_ingredients():
    return requests.get(f"{Urls.STELLAR_BURGERS_URL}{Urls.GET_INGREDIENTS}")

@allure.step('Создаю заказ')
def create_order(ingredients, access_token=None):
    headers = {}
    if access_token:
        headers["Authorization"] = access_token
    payload = {"ingredients": ingredients}
    return requests.post(f"{Urls.STELLAR_BURGERS_URL}{Urls.CREATE_ORDER}", json=payload, headers=headers)
