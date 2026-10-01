from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_transfer_request import UserTransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.models.base_model import ErrorResponse


class UserSteps(BaseSteps):

    def create_account(self, create_user_request: CreateUserRequest) -> BaseModel:
        """Позитивный шаг создания аккаунта"""
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.request_created()
        ).post()

    # --- ДЕПОЗИТ ---
    def user_deposit(self, create_user_request: CreateUserRequest, user_deposit):
        """Позитивный шаг депозита (200 OK)"""
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.USER_DEPOSIT,
            response_spec=ResponseSpecs.request_ok()
        ).post(user_deposit)

    def user_deposit_negative(self, create_user_request: CreateUserRequest, user_deposit):
        """Негативный шаг депозита: наполняет и проверяет статус 400 Bad Request внутри шага"""
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.USER_DEPOSIT,
            response_spec=ResponseSpecs.request_bad(),
            response_model=ErrorResponse
        ).post(user_deposit)

    # --- ПЕРЕВОД ---
    def user_transfer(self, create_user_request: CreateUserRequest, user_transfer: UserTransferRequest):
        """Позитивный шаг перевода (200 OK)"""
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            endpoint=Endpoint.USER_TRANSFER,
            response_spec=ResponseSpecs.request_ok()
        ).post(user_transfer)

    def user_transfer_negative(self, create_user_request: CreateUserRequest, user_transfer: UserTransferRequest):
        """Негативный шаг перевода: наполняет и проверяет статус 422 Unprocessable Entity внутри шага"""
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            endpoint=Endpoint.USER_TRANSFER,
            response_spec=ResponseSpecs.request_unprocessable(),
            response_model=ErrorResponse
        ).post(user_transfer)

    # --- ЗАПРОС КРЕДИТА ---
    def credit_request(self, create_user_request: CreateUserRequest, credit_request):
        """Позитивный шаг запроса кредита (201 Created)"""
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)

    def credit_request_negative(self, create_user_request: CreateUserRequest, credit_request):
        """Негативный шаг запроса кредита: наполняет и проверяет статус 400 Bad Request внутри шага"""
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.request_bad(),
            response_model=ErrorResponse
        ).post(credit_request)

    # --- ПОГАШЕНИЕ КРЕДИТА ---
    def credit_repay(self, create_user_request: CreateUserRequest, credit_repay):
        """Позитивный шаг погашения кредита (200 OK)"""
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            endpoint=Endpoint.CREDIT_REPAY,
            response_spec=ResponseSpecs.request_ok()
        ).post(credit_repay)

    def credit_repay_negative(self, create_user_request: CreateUserRequest, credit_repay):
        """Негативный шаг погашения кредита: наполняет и проверяет статус 422 Unprocessable Entity внутри шага"""
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
                role=create_user_request.role or "ROLE_USER"
            ),
            endpoint=Endpoint.CREDIT_REPAY,
            response_spec=ResponseSpecs.request_unprocessable(),
            response_model=ErrorResponse
        ).post(credit_repay)
