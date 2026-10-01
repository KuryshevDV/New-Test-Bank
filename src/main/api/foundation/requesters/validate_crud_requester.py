from typing import Optional
import allure
from pydantic import BaseModel
from src.main.api.configs.config import Config
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.requests.requester import Requester


class ValidateCrudRequester(Requester):

    def __init__(self, request_spec, endpoint, response_spec, response_model=None):
        # Базовый класс Requester требует строго определённую структуру с 'headers' и 'base_url'
        headers_dict = request_spec.get('headers', request_spec) if isinstance(request_spec,
                                                                               dict) and 'headers' in request_spec else request_spec

        formatted_spec = {
            'headers': headers_dict,
            'base_url': Config.fetch('backendUrl')
        }

        super().__init__(formatted_spec, response_spec)
        self.endpoint = endpoint
        self.response_spec = response_spec
        self.response_model = response_model  # Сохраняем кастомную модель ошибки, если она передана
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] = None) -> Optional[BaseModel]:
        # Метод post стал идеально чистым: никаких параметров из тестов!
        response = self.crud_requester.post(model)

        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")

        # Проверка статус-кода выполняется здесь, на уровне реквестера через переданную спеку
        self.response_spec(response)

        # Валидируем по кастомной модели ошибки (ErrorResponse), если она была задана в шаге, иначе по дефолтной успешной
        target_model = self.response_model if self.response_model is not None else self.endpoint.value.response_model
        return target_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        return response
