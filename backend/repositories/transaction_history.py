from backend.database.models import TransactionHistory
from backend.repositories.base import BaseRepository


class TransactionHistoryRepository(BaseRepository[TransactionHistory]):
    def __init__(self):
        super().__init__(TransactionHistory)


async def get_transaction_history_repository() -> TransactionHistoryRepository:
    return TransactionHistoryRepository()
