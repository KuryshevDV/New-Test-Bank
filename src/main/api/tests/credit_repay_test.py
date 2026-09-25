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
        credit_id, account_id, *credit_amount_opt = active_credit_data

        expected_full_amount = credit_amount_opt[0] if credit_amount_opt else 5000

        repay_payload = CreateRepayRequest(creditId=credit_id, accountId=account_id, amount=expected_full_amount)
        response = api_manager.user_steps.credit_repay(create_credit_user_request, repay_payload)

        assert response.creditId == credit_id, \
            f"Ожидали закрытие кредита с ID {credit_id}, но в ответе пришел ID: {response.creditId}"

        assert response.amountDeposited == repay_payload.amount, \
            f"Ожидали сумму погашения {repay_payload.amount}, но по факту зачислилось: {response.amountDeposited}"

    def test_credit_repay_partial_forbidden(self, db_session: Session, api_manager: ApiManager,
                                            create_credit_user_request: CreateUserRequest, active_credit_data: tuple):
        """Негативный тест: проверка бизнес-блокировки при попытке частичного погашения кредита"""
        credit_id, account_id, *credit_amount_opt = active_credit_data
        expected_full_amount = credit_amount_opt[0] if credit_amount_opt else 5000

        invalid_amount = expected_full_amount - 1000

        invalid_repay_payload = CreateRepayRequest(creditId=credit_id, accountId=account_id, amount=invalid_amount)

        expected_error = "The amount is not enough"

        try:
            api_manager.user_steps.credit_repay(create_credit_user_request, invalid_repay_payload)
            assert False, f"Ожидали ошибку валидации суммы '{expected_error}', но кредит успешно погасился частично"

        except AssertionError as exc:
            actual_error_text = str(exc)
            assert expected_error in actual_error_text, \
                f"Ожидали увидеть текст ошибки '{expected_error}', но по факту получили: '{actual_error_text}'"
