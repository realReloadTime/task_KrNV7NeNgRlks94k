from pydantic import BaseModel, ConfigDict


class CashAccountCreate(BaseModel):
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class CashAccountUpdate(BaseModel):
    balance: int


class CashAccountGet(CashAccountCreate):
    id: int
    user_id: int
    balance: float
