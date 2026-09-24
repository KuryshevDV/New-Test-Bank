from src.main.api.models.base_model import BaseModel


class UserDepositRequest(BaseModel):
    accountId: int
    amount: float