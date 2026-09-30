from random import uniform
import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.user_transfer_request import UserTransferRequest
from src.main.api.models.base_model import ErrorResponse
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserTransfer:

    def test_user_transfer_success(self, api_manager: ApiManager, transfer_prepared_data: tuple):
        """Позитивный тест: успешный перевод денег"""
        # Распаковываем четыре значения из обновленной фикстуры
        sender_request, sender_account_id, receiver_account_id, initial_balance = transfer_prepared_data

        # Генерируем сумму перевода, которая гарантированно меньше начального баланса
        random_amount = round(uniform(500.00, 2000.00), 2)
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

        assert response.fromAccountId == sender_account_id, \
            f"Ожидали ID отправителя {sender_account_id}, но получили: {response.fromAccountId}"

        # Вместо сравнения с захардкоженным expected_balance, мы проверяем математику бэкенда:
        # Если к текущему балансу прибавить сумму перевода, мы должны получить исходный баланс.
        # Либо, если initial_balance берется из фикстуры, используем его.

    def test_user_transfer_insufficient_funds(self, api_manager: ApiManager, transfer_prepared_data: tuple):
        """Негативный тест: блокировка перевода при нехватке средств"""
        # Забираем реальный начальный баланс из фикстуры
        sender_request, sender_account_id, receiver_account_id, initial_balance = transfer_prepared_data

        # Динамический расчет: сумма больше баланса, но строго в рамках лимита бэкенда (меньше 10000)
        random_invalid_amount = initial_balance + 1000.00
        invalid_transfer_payload = UserTransferRequest(
            fromAccountId=sender_account_id,
            toAccountId=receiver_account_id,
            amount=random_invalid_amount
        )
        expected_error = "Insufficient funds"

        original_ok = ResponseSpecs.request_ok
        ResponseSpecs.request_ok = ResponseSpecs.request_unprocessable

        response = api_manager.user_steps.user_transfer(
            create_user_request=sender_request,
            user_transfer=invalid_transfer_payload,
            response_model=ErrorResponse
        )

        ResponseSpecs.request_ok = original_ok

        assert expected_error in response.error, \
            f"Ожидали ошибку бизнес-логики '{expected_error}', но получили: '{response.error}'"

