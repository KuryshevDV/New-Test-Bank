import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreditRequest:

    def test_credit_request_success(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                    valid_credit_request):
        """Позитивный тест: успешное получение кредита (без рандома и расчетов в тесте)"""
        response = api_manager.user_steps.credit_request(create_credit_user_request, valid_credit_request)

        assert response.creditId is not None
        assert response.amount == valid_credit_request.amount

    def test_credit_request_amount_too_low(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                           invalid_credit_request):
        """Негативный тест: сумма ниже лимита (без рандома и расчетов в тесте)"""
        expected_error = "Amount must be between"
        response = api_manager.user_steps.credit_request_negative(create_credit_user_request, invalid_credit_request)
        assert expected_error in response.error
