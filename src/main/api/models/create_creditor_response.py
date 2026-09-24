from src.main.api.models.base_model import BaseModel
from pydantic import BaseModel, Field


class CreateCreditorResponse(BaseModel):
    accountId: int = Field(validation_alias='id')
    amount: float
    termMonths: int
    balance: float
    creditId: int