from src.main.api.models.base_model import BaseModel


class CreateRepayRequest(BaseModel):
    creditId: int
    accountId: int
    amount: int