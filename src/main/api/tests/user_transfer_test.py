import pytest
from src.main.api.classes.api_manager import ApiManager


@pytest.mark.api
class TestUserTransfer:

    def test_user_transfer_success(self, api_manager: ApiManager, transfer_prepared_data: tuple,
                                   valid_transfer_request):
        """Позитивный тест: успешный перевод (без рандома и расчетов в тесте)"""
        sender_request, sender_account_id, _, initial_balance = transfer_prepared_data
        expected_balance = initial_balance - valid_transfer_request.amount

        response = api_manager.user_steps.user_transfer(sender_request, valid_transfer_request)

        assert response.fromAccountId == sender_account_id
        assert float(response.fromAccountIdBalance) == float(expected_balance)

    def test_user_transfer_insufficient_funds(self, api_manager: ApiManager, transfer_prepared_data: tuple,
                                              invalid_transfer_request):
        """Негативный тест: блокировка перевода при нехватке средств (без рандома и расчетов в тесте)"""
        sender_request, _, _, _ = transfer_prepared_data
        expected_error = "Insufficient funds"

        response = api_manager.user_steps.user_transfer_negative(sender_request, invalid_transfer_request)
        assert expected_error in response.error
