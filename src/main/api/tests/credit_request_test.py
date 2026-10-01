import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_creditor_request import CreateCreditorRequest


@pytest.mark.api
class TestCreditRequest:

    def test_credit_request_success(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                    create_credit_account_id: int, valid_credit_data: tuple):
        """Позитивный тест: успешный кредит (без генерации в тесте)"""
        credit_amount, credit_term = valid_credit_data
        credit_payload = CreateCreditorRequest(accountId=create_credit_account_id, amount=credit_amount,
                                               termMonths=credit_term)

        response = api_manager.user_steps.credit_request(create_credit_user_request, credit_payload)
        assert response.creditId is not None
        assert response.amount == credit_payload.amount

    def test_credit_request_amount_too_low(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                           create_credit_account_id: int, invalid_credit_amount):
        """Негативный тест: сумма ниже лимита (без генерации в тесте)"""
        invalid_credit_payload = CreateCreditorRequest(accountId=create_credit_account_id, amount=invalid_credit_amount,
                                                       termMonths=12)
        expected_error = "Amount must be between"
        response = api_manager.user_steps.credit_request_negative(create_credit_user_request, invalid_credit_payload)
        assert expected_error in response.error
