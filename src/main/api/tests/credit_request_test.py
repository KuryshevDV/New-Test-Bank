from random import randint
import requests
import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_creditor_request import CreateCreditorRequest
from src.main.api.configs.config import Config
from src.main.api.specs.request_specs import RequestSpecs


@pytest.mark.api
class TestCreditRequest:

    def test_credit_request_success(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                    create_credit_account_id: int):
        """Позитивный тест: успешное получение кредита на валидную сумму от 5000 до 15000"""
        random_valid_amount = randint(5000, 15000)
        random_term = randint(3, 24)

        credit_payload = CreateCreditorRequest(accountId=create_credit_account_id, amount=random_valid_amount,
                                               termMonths=random_term)
        response = api_manager.user_steps.credit_request(create_credit_user_request, credit_payload)

        assert response.creditId is not None, \
            "Ожидали, что в ответе вернется сгенерированный ID кредита (creditId не должен быть None)"

        assert response.amount == credit_payload.amount, \
            f"Ожидали сумму одобренного кредита {credit_payload.amount}, но по факту пришло: {response.amount}"

    def test_credit_request_amount_too_low(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                           create_credit_account_id: int):
        """Негативный тест: проверка бизнес-блокировки при запросе суммы ниже минимального лимита (только степ и ассерт)"""
        random_low_amount = randint(100, 4999)
        random_term = randint(3, 24)

        invalid_credit_payload = CreateCreditorRequest(accountId=create_credit_account_id, amount=random_low_amount,
                                                       termMonths=random_term)
        expected_error = "Amount must be between"

        # ШАГ 1 (Степ): Прямой POST-запрос с заголовками авторизации фреймворка
        url = f"{Config.fetch('backendUrl')}/credit/request"
        headers = RequestSpecs.auth_headers(
            username=create_credit_user_request.username,
            password=create_credit_user_request.password
        )
        response = requests.post(url, json=invalid_credit_payload.model_dump(), headers=headers)

        # ШАГ 2 (Ассерты): Чистая проверка статус-кода 400 и сообщения об ошибке
        assert response.status_code == 400, \
            f"Ожидали статус-код 400 Bad Request, но получили {response.status_code}"

        actual_error = response.json().get("error")
        assert expected_error in actual_error, \
            f"Ожидали увидеть текст ошибки '{expected_error}', но по факту получили: '{actual_error}'"
