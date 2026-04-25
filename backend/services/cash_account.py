from backend.repositories.cash_account import CashAccountRepository
from backend.schemas.cash_account import CashAccountCreate, CashAccountUpdate, CashAccountGet


class CashAccountService:
    def __init__(self, cash_account_repository: CashAccountRepository):
        self.cash_account_repository = cash_account_repository

    async def create_cash_account(self, data: CashAccountCreate) -> CashAccountGet:
        return CashAccountGet.model_validate(await self.cash_account_repository.create(**data.model_dump()))

    async def get_cash_accounts_by_user_id(self, user_id: int) -> list[CashAccountGet]:
        return list(map(CashAccountGet.model_validate,
                        await self.cash_account_repository.get_by_fields_values([('user_id', user_id)])))

    async def get_cash_account_by_id(self, account_id: int) -> CashAccountGet | None:
        account = await self.cash_account_repository.get(account_id)
        if account is not None:
            return CashAccountGet.model_validate(account)
        return None

    async def update_cash_account(self, account_id: int, data: CashAccountUpdate) -> CashAccountGet:
        account = await self.cash_account_repository.get(account_id)
        if account is None:
            raise ValueError('Account not found')
        return CashAccountGet.model_validate(await self.cash_account_repository.update(account.id, **data.model_dump(exclude_unset=True)))

    async def delete_cash_account(self, account_id: int) -> bool:
        return await self.cash_account_repository.delete(account_id)


async def get_cash_account_service() -> CashAccountService:
    return CashAccountService(CashAccountRepository())
