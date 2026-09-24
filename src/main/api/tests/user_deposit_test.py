from random import randint
from requests import Session
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
import pytest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_deposit_request import UserDepositRequest

class TestUserDeposit:
    def test_user_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_user_id):
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=randint(a=100000, b=900000)/100)
        response = api_manager.user_steps.user_deposit(create_user_request, user_deposit_request)

        assert response.balance == user_deposit_request.amount

    def test_user_deposit_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_user_id):
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=-500.00)
        with pytest.raises(Exception) as exc_info:
            api_manager.user_steps.user_deposit(create_user_request, user_deposit_request)

        expected_error = "Amount must be greater than 0"
        assert expected_error in str(exc_info.value), f"Ожидали ошибку валидации суммы, но получили: {exc_info.value}"