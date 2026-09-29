import pytest
import requests
from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_repay_request import CreateRepayRequest
from src.main.api.configs.config import Config
from src.main.api.specs.request_specs import RequestSpecs


@pytest.mark.api
class TestCreditRepay:

    def test_credit_repay_full_success(self, db_session: Session, api_manager: ApiManager,
                                       create_credit_user_request: CreateUserRequest, active_credit_data: tuple):
        """Позитивный тест: успешное единовременное погашение кредита на всю сумму долга"""
        credit_id, account_id, *credit_amount_opt = active_credit_data
        expected_full_amount = credit_amount_opt[0] if credit_amount_opt else 5000

        repay_payload = CreateRepayRequest(creditId=credit_id, accountId=account_id, amount=expected_full_amount)
        response = api_manager.user_steps.credit_repay(create_credit_user_request, repay_payload)

        assert response.creditId == credit_id, \
            f"Ожидали закрытие кредита с ID {credit_id}, но в ответе пришел ID: {response.creditId}"

        assert response.amountDeposited == repay_payload.amount, \
            f"Ожидали сумму погашения {repay_payload.amount}, но по факту зачислилось: {response.amountDeposited}"

    def test_credit_repay_partial_forbidden(self, db_session: Session, api_manager: ApiManager,
                                            create_credit_user_request: CreateUserRequest, active_credit_data: tuple):
        """Негативный тест: проверка бизнес-блокировки при попытке частичного погашения кредита (только степ и ассерт)"""
        credit_id, account_id, *credit_amount_opt = active_credit_data
        expected_full_amount = credit_amount_opt[0] if credit_amount_opt else 5000
        invalid_amount = expected_full_amount - 1000

        invalid_repay_payload = CreateRepayRequest(creditId=credit_id, accountId=account_id, amount=invalid_amount)
        expected_error = "The amount is not enough"

        # ШАГ 1 (Степ): Прямой POST-запрос с заголовками авторизации фреймворка
        url = f"{Config.fetch('backendUrl')}/credit/repay"
        headers = RequestSpecs.auth_headers(
            username=create_credit_user_request.username,
            password=create_credit_user_request.password
        )
        response = requests.post(url, json=invalid_repay_payload.model_dump(), headers=headers)

        # ШАГ 2 (Ассерты): Чистая проверка статус-кода 400 и сообщения об ошибке
        assert response.status_code == 422, \
            f"Ожидали статус-код 422 Unprocessable Entity, но получили {response.status_code}"

        actual_error = response.json().get("error")
        assert expected_error in actual_error, \
            f"Ожидали увидеть текст ошибки '{expected_error}', но по факту получили: '{actual_error}'"
