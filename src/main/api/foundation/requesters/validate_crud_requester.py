from typing import Optional
import allure
from pydantic import BaseModel
from src.main.api.configs.config import Config
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.requests.requester import Requester


class ValidateCrudRequester(Requester):

    def __init__(self, request_spec, endpoint, response_spec):
        from src.main.api.configs.config import Config

        # Защищенное извлечение словаря заголовков:
        if isinstance(request_spec, dict) and 'headers' in request_spec:
            headers_dict = request_spec['headers']
        else:
            headers_dict = request_spec

        formatted_spec = {
            'headers': headers_dict,
            'base_url': Config.fetch('backendUrl')
        }

        super().__init__(formatted_spec, response_spec)
        self.endpoint = endpoint
        self.response_spec = response_spec
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] = None, response_spec=None, response_model=None) -> Optional[BaseModel]:
        active_spec = response_spec if response_spec is not None else self.response_spec
        self.crud_requester.response_spec = active_spec

        response = self.crud_requester.post(model)

        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")

        active_spec(response)

        target_model = response_model if response_model is not None else self.endpoint.value.response_model
        return target_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        return response
