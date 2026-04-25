from hashlib import sha256

from backend.repositories.transaction_history import TransactionHistoryRepository
from backend.schemas.cash_account import CashAccountCreate
from backend.schemas.transaction_history import TransactionHistoryCreate, TransactionHistoryGet, TransactionHistoryInput

from backend.services.cash_account import CashAccountService, get_cash_account_service

from backend.settings import settings


class TransactionHistoryService():
    def __init__(self, repository: TransactionHistoryRepository, cash_account_service: CashAccountService):
        self.transaction_history_repository = repository
        self.cash_account_service = cash_account_service

    async def is_signature_valid(self, data: TransactionHistoryInput) -> bool:
        line = f'{data.account_id}{data.amount}{data.transaction_id}{data.user_id}{settings.SECRET_KEY}'.encode('utf-8')
        return sha256(line).hexdigest() == data.signature

    async def create_transaction(self, data: TransactionHistoryInput) -> TransactionHistoryGet:
        assert await self.is_signature_valid(data)
        account = await self.cash_account_service.get_cash_account_by_id(data.account_id)
        if account is None:
            account = await self.cash_account_service.create_cash_account(CashAccountCreate(user_id=data.user_id))
        return TransactionHistoryGet.model_validate(await self.transaction_history_repository.create(
            **TransactionHistoryCreate(
                cash_account_id=account.id,
                side_transaction_id=data.transaction_id,
                amount=data.amount
            ).model_dump()))

    async def get_transaction_history_by_cash_account_id(self, account_id: int) -> list[TransactionHistoryGet]:
        return list(map(TransactionHistoryGet.model_validate,
                        await self.transaction_history_repository.get_by_fields_values(
                            [('cash_account_id', account_id)])))

    async def get_transaction_history_by_user_id(self, user_id: int) -> list[TransactionHistoryGet]:
        return list(map(TransactionHistoryGet.model_validate,
                        await self.transaction_history_repository.get_by_fields_values(
                            [('cash_account.user_id', user_id)])))


async def get_transaction_history_service():
    return TransactionHistoryService(TransactionHistoryRepository(), await get_cash_account_service())
