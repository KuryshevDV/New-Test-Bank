from random import uniform
import requests
import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.user_transfer_request import UserTransferRequest
from src.main.api.configs.config import Config
from src.main.api.specs.request_specs import RequestSpecs


@pytest.mark.api
class TestUserTransfer:

    def test_user_transfer_success(self, api_manager: ApiManager, transfer_prepared_data: tuple):
        """Позитивный тест: успешный перевод денег"""
        sender_request, sender_account_id, receiver_account_id = transfer_prepared_data

        # Диапазон строго по правилам бэкенда: от 500 до 5000
        random_amount = round(uniform(500.00, 5000.00), 2)
        initial_balance = 6000.00
        expected_balance = initial_balance - random_amount

        transfer_payload = UserTransferRequest(
            fromAccountId=sender_account_id,
            toAccountId=receiver_account_id,
            amount=random_amount
        )
        response = api_manager.user_steps.user_transfer(sender_request, transfer_payload)

        assert response.fromAccountId == sender_account_id, \
            f"Ожидали ID отправителя {sender_account_id}, но получили: {response.fromAccountId}"

        assert float(response.fromAccountIdBalance) == float(expected_balance), \
            f"Ожидали остаток {expected_balance}, но получили: {response.fromAccountIdBalance}"

    def test_user_transfer_insufficient_funds(self, api_manager: ApiManager, transfer_prepared_data: tuple):
        """Негативный тест: блокировка перевода при нехватке средств (только степ и ассерт)"""
        sender_request, sender_account_id, receiver_account_id = transfer_prepared_data
        random_invalid_amount = round(uniform(7000.00, 10000.00), 2)

        invalid_transfer_payload = UserTransferRequest(
            fromAccountId=sender_account_id,
            toAccountId=receiver_account_id,
            amount=random_invalid_amount
        )
        expected_error = "Insufficient funds"

        # СТЕП: Отправляем прямой POST-запрос с авторизацией из фреймворка
        url = f"{Config.fetch('backendUrl')}/account/transfer"
        headers = RequestSpecs.auth_headers(
            username=sender_request.username,
            password=sender_request.password,
            role=sender_request.role or "ROLE_USER"
        )
        response = requests.post(url, json=invalid_transfer_payload.model_dump(), headers=headers)

        # АССЕРТЫ: Проверяем статус 422 и текст ошибки бизнес-логики напрямую из JSON
        assert response.status_code == 422, \
            f"Ожидали статус-код 422 Unprocessable Entity, но получили {response.status_code}"

        actual_error = response.json().get("error")
        assert expected_error in actual_error, \
            f"Ожидали ошибку '{expected_error}', но бэкенд вернул: '{actual_error}'"
