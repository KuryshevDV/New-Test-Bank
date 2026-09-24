import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_creditor_request import CreateCreditorRequest


@pytest.mark.api
class TestCreditRequest:

    def test_credit_request_success(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                    create_credit_account_id: int):
        """Позитивный тест: успешное получение кредита на минимально допустимую сумму (5000)"""

        # Act: Формируем и отправляем запрос на получение кредита (сумма int)
        credit_payload = CreateCreditorRequest(accountId=create_credit_account_id, amount=5000, termMonths=12)
        response = api_manager.user_steps.credit_request(create_credit_user_request, credit_payload)

        # Assert: Проверяем валидность бизнес-ответа API
        assert response.creditId is not None
        assert response.amount == 5000

    def test_credit_request_amount_too_low(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                           create_credit_account_id: int):
        """Негативный тест: проверка бизнес-блокировки при запросе суммы ниже лимита (4000 вместо 5000)"""

        # Нарушаем лимит ТЗ: запрашиваем 4000
        invalid_credit_payload = CreateCreditorRequest(accountId=create_credit_account_id, amount=4000, termMonths=12)

        # Act & Assert: Ожидаем блокировку операции бизнес-логикой бэкенда (400 Bad Request)
        with pytest.raises(Exception) as exc_info:
            api_manager.user_steps.credit_request(create_credit_user_request, invalid_credit_payload)

        # Сверяем с текстом ошибки валидации лимитов бэкенда
        assert "Amount must be between" in str(exc_info.value), f"Получили неожиданную ошибку: {exc_info.value}"
