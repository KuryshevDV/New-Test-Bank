from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_deposit_request import UserDepositRequest


class TestUserDeposit:

    def test_user_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                          create_account_user_id, valid_deposit_amount):
        """Позитивный тест: успешный депозит (без генерации в тесте)"""
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=valid_deposit_amount)
        response = api_manager.user_steps.user_deposit(create_user_request, user_deposit_request)
        assert response.balance == user_deposit_request.amount

    def test_user_deposit_invalid(self, db_session: Session, api_manager: ApiManager,
                                  create_user_request: CreateUserRequest, create_account_user_id,
                                  invalid_deposit_amount):
        """Негативный тест: блокировка депозита (без генерации в тесте)"""
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=invalid_deposit_amount)
        expected_error = "Amount must be greater than 0"
        response = api_manager.user_steps.user_deposit_negative(create_user_request, user_deposit_request)
        assert expected_error in response.error
