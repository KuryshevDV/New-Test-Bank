from pydantic import BaseModel as BM


class BaseModel(BM):
    ...


class ErrorResponse(BaseModel):
    error: str
