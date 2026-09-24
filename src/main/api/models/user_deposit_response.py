from src.main.api.models.base_model import BaseModel


class UserDepositResponse(BaseModel):
    id: int
    balance: float