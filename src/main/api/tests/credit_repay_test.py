import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreditRepay:

    def test_credit_repay_full_success(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                       active_credit_data: tuple, valid_repay_request):
        """Позитивный тест: успешное полное погашение кредита (без рандома и расчетов в тесте)"""
        credit_id, _, _ = active_credit_data
        response = api_manager.user_steps.credit_repay(create_credit_user_request, valid_repay_request)

        assert response.creditId == credit_id
        assert response.amountDeposited == valid_repay_request.amount

    def test_credit_repay_partial_forbidden(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                            invalid_repay_request):
        """Негативный тест: блокировка частичного погашения (без рандома и расчетов в тесте)"""
        expected_error = "The amount is not enough"
        response = api_manager.user_steps.credit_repay_negative(create_credit_user_request, invalid_repay_request)
        assert expected_error in response.error
