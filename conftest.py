import pytest

from helpers import generate_user_data, courier_delete, courier_creation_and_return_login_password


@pytest.fixture
def delete_user_after_test():
    user_tokens = []
    yield user_tokens
    for access_token in user_tokens:
        if access_token:
            courier_delete(access_token)






@pytest.fixture
def create_courier_and_registration():
    courier_data = generate_courier_data()
    new_courier = courier_creation_and_return_login_password(courier_data)
    assert new_courier is not None
    return courier_data
