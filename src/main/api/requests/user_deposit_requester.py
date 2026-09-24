from http import HTTPStatus

import requests
from requests import Response
from src.main.api.models.user_deposit_request import UserDepositRequest
from src.main.api.models.user_deposit_response import UserDepositResponse
from src.main.api.requests.requester import Requester




class UserDepositRequester(Requester):
    def post(self, user_deposit_request: UserDepositRequest) -> UserDepositResponse | Response:
        url=f"{self.base_url}/account/deposit"
        response = requests.post(
            url=url,
            json=user_deposit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code [HTTPStatus.OK, HTTPStatus.CREATED]:
            return UserDepositResponse(**response.json())
        return response