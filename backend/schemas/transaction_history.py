from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TransactionHistoryCreate(BaseModel):
    cash_account_id: int
    side_transaction_id: str

    amount: float

    model_config = ConfigDict(from_attributes=True)


class TransactionHistoryGet(TransactionHistoryCreate):
    id: int
    account_user_id: int

    created_at: datetime


class TransactionHistoryInput(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: float
    signature: str
