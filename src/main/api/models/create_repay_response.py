from src.main.api.models.base_model import BaseModel


class CreateRepayResponse(BaseModel):
    creditId: int
    amountDeposited: int
