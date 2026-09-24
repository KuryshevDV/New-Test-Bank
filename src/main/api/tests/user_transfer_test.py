import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.user_transfer_request import UserTransferRequest


@pytest.mark.api
class TestUserTransfer:

    def test_user_transfer_success(self, api_manager: ApiManager, transfer_prepared_data: tuple):
        """Позитивный тест: успешный перевод 2000.00 рублей между клиентами банка"""
        sender_request, sender_account_id, receiver_account_id = transfer_prepared_data

        # Act: Сборка payload и выполнение запроса перевода денег (передаем float)
        transfer_payload = UserTransferRequest(
            fromAccountId=sender_account_id,
            toAccountId=receiver_account_id,
            amount=2000.00
        )
        response = api_manager.user_steps.user_transfer(sender_request, transfer_payload)

        # Assert по API согласно Swagger: принудительно приводим к float обе части,
        # чтобы типы данных (int/float) на бэкенде больше не ломали ассерт
        assert response.fromAccountId == sender_account_id
        assert float(response.fromAccountIdBalance) == float(4000.00)

    def test_user_transfer_insufficient_funds(self, api_manager: ApiManager, transfer_prepared_data: tuple):
        """Негативный тест: блокировка перевода при нехватке средств на балансе (8000.00 при балансе 6000.00)"""
        sender_request, sender_account_id, receiver_account_id = transfer_prepared_data

        # Нарушаем правила: запрашиваем сумму больше доступного остатка
        invalid_transfer_payload = UserTransferRequest(
            fromAccountId=sender_account_id,
            toAccountId=receiver_account_id,
            amount=8000.00
        )

        # Act & Assert: Ожидаем блокировку операции бизнес-логикой бэкенда (400 Bad Request)
        with pytest.raises(Exception) as exc_info:
            api_manager.user_steps.user_transfer(sender_request, invalid_transfer_payload)

        # Проверяем текст ошибки бизнес-логики о нехватке денег на бэкенде
        assert "Insufficient funds" in str(exc_info.value), f"Получили неожиданную ошибку: {exc_info.value}"
