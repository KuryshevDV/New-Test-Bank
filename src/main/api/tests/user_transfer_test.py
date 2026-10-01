import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.user_transfer_request import UserTransferRequest


@pytest.mark.api
class TestUserTransfer:

    def test_user_transfer_success(self, api_manager: ApiManager, transfer_prepared_data: tuple, valid_transfer_amount):
        """Позитивный тест: успешный перевод (без генерации в тесте)"""
        sender_request, sender_account_id, receiver_account_id, initial_balance = transfer_prepared_data
        expected_balance = initial_balance - valid_transfer_amount

        transfer_payload = UserTransferRequest(
            fromAccountId=sender_account_id,
            toAccountId=receiver_account_id,
            amount=valid_transfer_amount
        )
        response = api_manager.user_steps.user_transfer(sender_request, transfer_payload)

        assert response.fromAccountId == sender_account_id
        assert float(response.fromAccountIdBalance) == float(expected_balance)

    def test_user_transfer_insufficient_funds(self, api_manager: ApiManager, transfer_prepared_data: tuple,
                                              invalid_transfer_amount):
        """Негативный тест: блокировка перевода (без генерации в тесте)"""
        sender_request, sender_account_id, receiver_account_id, _ = transfer_prepared_data

        invalid_transfer_payload = UserTransferRequest(
            fromAccountId=sender_account_id,
            toAccountId=receiver_account_id,
            amount=invalid_transfer_amount
        )
        expected_error = "Insufficient funds"
        response = api_manager.user_steps.user_transfer_negative(sender_request, invalid_transfer_payload)
        assert expected_error in response.error
