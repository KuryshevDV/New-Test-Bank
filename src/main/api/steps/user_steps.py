from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models import user_deposit_request
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_creditor_request import CreateCreditorRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_transfer_request import UserTransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest) -> BaseModel:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def user_deposit(self, create_user_request: CreateUserRequest, user_deposit):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.USER_DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(user_deposit)
        return response

    def user_transfer(self, create_user_request: CreateUserRequest, user_transfer: UserTransferRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            Endpoint.USER_TRANSFER,
            ResponseSpecs.request_ok()
        ).post(user_transfer)
        return response

    def credit_request(self, create_creditor_request: CreateCreditorRequest, credit_account):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_creditor_request.username,
                password=create_creditor_request.password,
                role="ROLE_CREDIT_SECRET"
            ),
            Endpoint.CREDIT_ACCOUNT,
            ResponseSpecs.request_created()
        ).post(credit_account)
        return response

    def credit_repay(self, create_creditor_request: CreateCreditorRequest, credit_repay):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_creditor_request.username,
                password=create_creditor_request.password,
                role=create_creditor_request.role
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay)
        return response










