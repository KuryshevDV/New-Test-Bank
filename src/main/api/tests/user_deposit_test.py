from random import uniform
from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_deposit_request import UserDepositRequest
from src.main.api.models.base_model import ErrorResponse
from src.main.api.specs.response_specs import ResponseSpecs


class TestUserDeposit:
    def test_user_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                          create_account_user_id):
        """Позитивный тест: успешный депозит случайной валидной суммы"""
        random_valid_amount = round(uniform(1000.00, 9000.00), 2)
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=random_valid_amount)

        response = api_manager.user_steps.user_deposit(create_user_request, user_deposit_request)

        assert response.balance == user_deposit_request.amount, \
            f"Ожидали, что баланс станет {user_deposit_request.amount}, но по факту получили: {response.balance}"

    def test_user_deposit_invalid(self, db_session: Session, api_manager: ApiManager,
                                  create_user_request: CreateUserRequest, create_account_user_id):
        """Негативный тест: блокировка депозита на отрицательную сумму"""
        random_invalid_amount = round(uniform(-1000.00, -1.00), 2)
        user_deposit_request = UserDepositRequest(accountId=create_account_user_id, amount=random_invalid_amount)

        expected_error = "Amount must be greater than 0"

        # СТЕП: Передаем спецификацию 400 ошибки и модель ErrorResponse в аргументы метода шага
        response = api_manager.user_steps.user_deposit(
            create_user_request=create_user_request,
            user_deposit=user_deposit_request,
            response_spec=ResponseSpecs.request_bad(),
            response_model=ErrorResponse
        )

        # АССЕРТ: Статус-код проверился автоматически внутри спеки, проверяем только текст бизнес-ошибки
        assert expected_error in response.error, \
            f"Ожидали ошибку валидации '{expected_error}', но бэкенд вернул: '{response.error}'"
