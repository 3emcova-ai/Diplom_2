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

@allure.step('Получаю accessToken зарегистрированного пользователя')
def user_get_access_token(email, password):
    response_access_token = user_login(email, password)
    if response_access_token.status_code == 200:
        return response_access_token.json()['accessToken']
    return None

@allure.step('Удаляю пользователя')
def user_delete(access_token):
    return requests.delete(f'{Urls.STELLAR_BURGERS_URL}{Urls.DELETE_USER}/{access_token}')

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






@allure.step('Осуществляю авторизацию пользователя')
def courier_login(login, password):
    return requests.post(f'{Urls.SCOOTER_URL}{Urls.LOGIN_COURIER}', json={
    'login': login,
    'password': password
    })

@allure.step('Получаю id зарегистрированного курьера')
def courier_get_id(login, password):
    response_courier_id = courier_login(login, password)
    if response_courier_id.status_code == 200:
        return response_courier_id.json()['id']
    return None

@allure.step('Удаляю курьера')
def courier_delete(courier_id):
    return requests.delete(f'{Urls.SCOOTER_URL}{Urls.DELETE_COURIER}/{courier_id}')

@allure.step('Регистрирую курьера и возвращаю список из логина и пароля')
def courier_creation_and_return_login_password(courier_data):
    response = requests.post(f'{Urls.SCOOTER_URL}{Urls.CREATE_COURIER}', json=courier_data)
    if response.status_code == 201:
        return (courier_data['login'], courier_data['password'])
    return None 
