import pytest
from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_repay_request import CreateRepayRequest
from src.main.api.models.base_model import ErrorResponse
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRepay:

    def test_credit_repay_full_success(self, db_session: Session, api_manager: ApiManager,
                                       create_credit_user_request: CreateUserRequest, active_credit_data: tuple):
        """Позитивный тест: успешное единовременное погашение кредита на всю сумму долга"""
        # Динамически распаковываем данные из фикстуры, исключая хардкод
        credit_id, account_id, credit_amount = active_credit_data

        repay_payload = CreateRepayRequest(creditId=credit_id, accountId=account_id, amount=credit_amount)
        response = api_manager.user_steps.credit_repay(create_credit_user_request, repay_payload)

        assert response.creditId == credit_id, \
            f"Ожидали закрытие кредита с ID {credit_id}, но в ответе пришел ID: {response.creditId}"

        assert response.amountDeposited == repay_payload.amount, \
            f"Ожидали сумму погашения {repay_payload.amount}, но по факту зачислилось: {response.amountDeposited}"

    def test_credit_repay_partial_forbidden(self, db_session: Session, api_manager: ApiManager,
                                            create_credit_user_request: CreateUserRequest, active_credit_data: tuple,
                                            invalid_repay_amount):
        """Негативный тест: проверка бизнес-блокировки при попытке частичного погашения кредита"""
        credit_id, account_id, _ = active_credit_data

        invalid_repay_payload = CreateRepayRequest(creditId=credit_id, accountId=account_id,
                                                   amount=invalid_repay_amount)
        expected_error = "The amount is not enough"

        # СТЕП: Вызываем правильный негативный метод без передачи спек напрямую из теста
        response = api_manager.user_steps.credit_repay_negative(create_credit_user_request, invalid_repay_payload)

        # АССЕРТ
        assert expected_error in response.error, \
            f"Ожидали увидеть текст ошибки '{expected_error}', но по факту получили: '{response.error}'"

