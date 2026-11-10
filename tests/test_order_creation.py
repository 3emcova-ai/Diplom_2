import allure

from data import ResponseMessages, TestData
from helpers import create_order


class TestOrderCreation:

    @allure.title("Создание заказа авторизованным пользователем")
    def test_order_create_authoriz_user(self, create_registred_delete_user, return_ingredients):
        user_data = create_registred_delete_user["data"]
        access_token = create_registred_delete_user["token"]
        response_order = create_order(return_ingredients, access_token)
        assert response_order.status_code == 200
        assert response_order.json()["success"] is True
        order_owner = response_order.json()["order"]["owner"]
        assert order_owner["email"] == user_data["email"]
        assert order_owner["name"] == user_data["name"]
                
    @allure.title("Создание заказа не авторизованным пользователем")
    def test_order_create_unauthoriz_user(self, return_ingredients):
        response_order = create_order(return_ingredients)
        assert response_order.status_code == 200
        assert response_order.json()["success"] is True
        assert response_order.json()["order"].get("owner") is None

    @allure.title("Создание заказа c ингредиентами авторизованным пользователем")
    def test_order_create_authoriz_user_with_ingr(self, create_registred_delete_user, return_ingredients):
        access_token = create_registred_delete_user["token"]
        response_order = create_order(return_ingredients, access_token)
        assert response_order.status_code == 200
        assert response_order.json()["success"] is True
        order_ingredients = response_order.json()["order"]["ingredients"]
        assert len(order_ingredients) > 0
        
    @allure.title("Создание заказа без ингредиентов авторизованным пользователем")
    def test_order_create_authoriz_user_without_ingr_shows_error(self, create_registred_delete_user):
        access_token = create_registred_delete_user["token"]
        response_order = create_order([], access_token)
        assert response_order.status_code == 400
        assert response_order.json()["success"] is False
        assert response_order.json()["message"] == ResponseMessages.ERROR_ORDER_WITHOUT_INGREDIENTS
        
    @allure.title("Создание заказа с неверным хешем ингредиента авторизованным пользователем")
    def test_order_create_authoriz_user_with_invalid_ingr_shows_error(self, create_registred_delete_user):
        access_token = create_registred_delete_user["token"]
        incorrect_ingr = TestData.INCORRECT_INGR    
        response_order = create_order([incorrect_ingr], access_token)
        assert response_order.status_code == 400
        assert response_order.json()["success"] is False
        assert response_order.json()["message"] == ResponseMessages.ERROR_INCORRECT_INGREDIENT
        