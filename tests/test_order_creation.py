import allure

from data import ResponseMessages
from helpers import get_ingredients, create_order


class TestOrderCreation:

    @allure.title("Создание заказа авторизованным пользователем")
    def test_order_create_authoriz_user(self, registered_user, return_ingredients, delete_user_after_test):
        user_data = registered_user["data"]
        access_token = registered_user["token"]
        response_order = create_order(return_ingredients, access_token)
        assert response_order.status_code == 200
        assert response_order.json()["success"] is True
        order_owner = response_order.json()["order"]["owner"]
        assert order_owner["email"] == user_data["email"]
        assert order_owner["name"] == user_data["name"]
        delete_user_after_test.append(access_token)
        
    @allure.title("Создание заказа не авторизованным пользователем")
    def test_order_create_unauthoriz_user(self):
        response_ingredients = get_ingredients()
        assert response_ingredients.status_code == 200
        ingredients_data = response_ingredients.json()["data"]
        ingredient_ids = [ingredients_data[0]["_id"], ingredients_data[1]["_id"]]
        response_order = create_order(ingredient_ids)
        assert response_order.status_code == 200
        assert response_order.json()["success"] is True
        assert response_order.json()["order"].get("owner") is None

    @allure.title("Создание заказа c ингредиентами авторизованным пользователем")
    def test_order_create_authoriz_user_with_ingr(self, registered_user, return_ingredients, delete_user_after_test):
        access_token = registered_user["token"]
        response_order = create_order(return_ingredients, access_token)
        assert response_order.status_code == 200
        assert response_order.json()["success"] is True
        order_ingredients = response_order.json()["order"]["ingredients"]
        assert len(order_ingredients) > 0
        delete_user_after_test.append(access_token)

    @allure.title("Создание заказа без ингредиентов авторизованным пользователем")
    def test_order_create_authoriz_user_without_ingr_shows_error(self, registered_user, delete_user_after_test):
        access_token = registered_user["token"]
        response_order = create_order([], access_token)
        assert response_order.status_code == 400
        assert response_order.json()["success"] is False
        assert response_order.json()["message"] == ResponseMessages.ERRORR_ORDER_WITHOUT_INGREDIENTS
        delete_user_after_test.append(access_token)

    @allure.title("Создание заказа с неверным хешем ингредиента авторизованным пользователем")
    def test_order_create_authoriz_user_with_invalid_ingr_shows_error(self, registered_user, delete_user_after_test):
        access_token = registered_user["token"]
        invalid_ingr = "66ccc55777ddf000000aaa00"    
        response_order = create_order([invalid_ingr], access_token)
        assert response_order.status_code == 500
        delete_user_after_test.append(access_token)
