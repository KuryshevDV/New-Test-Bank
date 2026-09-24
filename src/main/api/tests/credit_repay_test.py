import pytest
from requests import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_repay_request import CreateRepayRequest


@pytest.mark.api
class TestCreditRepay:

    def test_credit_repay_full_success(self, db_session: Session, api_manager: ApiManager,
                                       create_credit_user_request: CreateUserRequest, active_credit_data: tuple):
        """Позитивный тест: успешное единовременное погашение кредита на всю сумму долга"""
        credit_id, account_id = active_credit_data

        # Act: Отправляем запрос на полное погашение (5000)
        repay_payload = CreateRepayRequest(creditId=credit_id, accountId=account_id, amount=5000)
        response = api_manager.user_steps.credit_repay(create_credit_user_request, repay_payload)

        # Assert: Проверяем валидность ответа API (успешное закрытие сущности кредита на бэкенде)
        assert response.creditId == credit_id
        assert response.amountDeposited == 5000

    def test_credit_repay_partial_forbidden(self, db_session: Session, api_manager: ApiManager,
                                            create_credit_user_request: CreateUserRequest, active_credit_data: tuple):
        """Негативный тест: проверка бизнес-блокировки при попытке частичного погашения кредита"""
        credit_id, account_id = active_credit_data

        # Пытаемся внести частичную сумму 2000 вместо 5000
        invalid_repay_payload = CreateRepayRequest(creditId=credit_id, accountId=account_id, amount=2000)

        with pytest.raises(Exception) as exc_info:
            api_manager.user_steps.credit_repay(create_credit_user_request, invalid_repay_payload)

        assert "The amount is not enough" in str(exc_info.value), f"Получили неожиданную ошибку: {exc_info.value}"
