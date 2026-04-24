from backend.database.models import CashAccount
from backend.repositories.base import BaseRepository


class CashAccountRepository(BaseRepository[CashAccount]):
    def __init__(self):
        super().__init__(CashAccount)


async def get_cash_account_repository() -> CashAccountRepository:
    return CashAccountRepository()
