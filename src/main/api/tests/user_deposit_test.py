from random import randint, uniform
from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_deposit_request import UserDepositRequest


class TestUserDeposit:
    def test_user_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                          create_account_user_id):
        random_amount = round(uniform(1000.00, 9000.00), 2)
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=random_amount)

        response = api_manager.user_steps.user_deposit(create_user_request, user_deposit_request)

        assert response.balance == user_deposit_request.amount, \
            f"Ожидали баланс {user_deposit_request.amount}, но получили {response.balance}"

    def test_user_deposit_invalid(self, db_session: Session, api_manager: ApiManager,
                              create_user_request: CreateUserRequest, create_account_user_id):
        random_invalid_amount = round(uniform(-1000.00, -1.00), 2)
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=random_invalid_amount)

        expected_error = "Amount must be greater than 0"

        try:
            api_manager.user_steps.user_deposit(create_user_request, user_deposit_request)
            assert False, f"Ожидали ошибку валидации '{expected_error}', но запрос завершился успешно со статусом 200"

        except AssertionError as exc:
            actual_error_text = str(exc)
            assert expected_error in actual_error_text, \
                f"Ожидали ошибку '{expected_error}', но по факту получили: '{actual_error_text}'"

