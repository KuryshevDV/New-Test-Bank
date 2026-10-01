from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest


class TestUserDeposit:

    def test_user_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                          valid_deposit_request):
        """Позитивный тест: успешный депозит (без рандома и расчетов в тесте)"""
        response = api_manager.user_steps.user_deposit(create_user_request, valid_deposit_request)
        assert response.balance == valid_deposit_request.amount

    def test_user_deposit_invalid(self, db_session: Session, api_manager: ApiManager,
                                  create_user_request: CreateUserRequest, invalid_deposit_request):
        """Негативный тест: блокировка депозита на отрицательную сумму (без рандома и расчетов в тесте)"""
        expected_error = "Amount must be greater than 0"
        response = api_manager.user_steps.user_deposit_negative(create_user_request, invalid_deposit_request)
        assert expected_error in response.error
