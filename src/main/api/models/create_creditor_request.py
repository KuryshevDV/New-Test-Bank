from src.main.api.models.base_model import BaseModel


class CreateCreditorRequest(BaseModel):
    accountId: int
    amount: float
    termMonths: int