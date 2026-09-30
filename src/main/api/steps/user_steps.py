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

    def user_deposit(self, create_user_request: CreateUserRequest, user_deposit, response_spec=None, response_model=None):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.USER_DEPOSIT,
            response_spec=ResponseSpecs.request_ok()
        ).post(user_deposit, response_spec=response_spec, response_model=response_model)
        return response

    def user_transfer(self, create_user_request: CreateUserRequest, user_transfer: UserTransferRequest, response_spec=None, response_model=None):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            endpoint=Endpoint.USER_TRANSFER,
            response_spec=ResponseSpecs.request_ok()
        ).post(user_transfer, response_spec=response_spec, response_model=response_model)
        return response

    def credit_request(self, create_user_request: CreateUserRequest, credit_request, response_spec=None, response_model=None):
        active_spec = response_spec if response_spec is not None else ResponseSpecs.request_created()
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=active_spec
        ).post(credit_request, response_spec=response_spec, response_model=response_model)
        return response

    def credit_repay(self, create_user_request: CreateUserRequest, credit_repay, response_spec=None, response_model=None):
        active_spec = response_spec if response_spec is not None else ResponseSpecs.request_ok()
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            endpoint=Endpoint.CREDIT_REPAY,
            response_spec=active_spec
        ).post(credit_repay, response_spec=response_spec, response_model=response_model)
        return response











