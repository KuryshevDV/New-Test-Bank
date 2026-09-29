from random import uniform
from requests import Session
import requests
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_deposit_request import UserDepositRequest
from src.main.api.configs.config import Config
from src.main.api.specs.request_specs import RequestSpecs


class TestUserDeposit:
    def test_user_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                          create_account_user_id):
        """Позитивный тест: успешный депозит случайной валидной суммы"""
        random_valid_amount = round(uniform(1000.00, 9000.00), 2)
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=random_valid_amount)

        response = api_manager.user_steps.user_deposit(create_user_request, user_deposit_request)

        assert response.balance == user_deposit_request.amount, \
            f"Ожидали, что баланс станет {user_deposit_request.amount}, но по факту получили: {response.balance}"

    def test_user_deposit_invalid(self, db_session: Session, api_manager: ApiManager,
                                  create_user_request: CreateUserRequest, create_account_user_id):
        """Негативный тест: блокировка депозита на отрицательную сумму (только степ и ассерт)"""
        random_invalid_amount = round(uniform(-1000.00, -1.00), 2)
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=random_invalid_amount)

        expected_error = "Amount must be greater than 0"

        # ШАГ 1 (Степ): Прямой POST-запрос с авторизацией из фреймворка в обход Pydantic-валидатора
        url = f"{Config.fetch('backendUrl')}/account/deposit"
        headers = RequestSpecs.auth_headers(
            username=create_user_request.username,
            password=create_user_request.password
        )
        response = requests.post(url, json=user_deposit_request.model_dump(), headers=headers)

        # ШАГ 2 (Ассерты): Прямая и чистая проверка статус-кода 400 и текста ошибки напрямую из JSON
        assert response.status_code == 400, \
            f"Ожидали статус-код 400 Bad Request, но получили {response.status_code}"

        actual_error = response.json().get("error")
        assert expected_error in actual_error, \
            f"Ожидали ошибку валидации '{expected_error}', но бэкенд вернул: '{actual_error}'"
