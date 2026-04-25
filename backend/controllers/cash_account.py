from fastapi import APIRouter, Depends, status, HTTPException

from backend.database.enums import RoleEnum

from backend.schemas.cash_account import CashAccountUpdate, CashAccountGet, CashAccountCreate

from backend.security.authorization import require_current_user, require_roles
from backend.services.cash_account import get_cash_account_service, CashAccountService

router = APIRouter(prefix="/cash-accounts", tags=["Cash account"])


@router.post("/create", response_model=CashAccountGet)
async def create_cash_account(
        current_user=Depends(require_current_user),
        service: CashAccountService = Depends(get_cash_account_service)):
    try:
        return await service.create_cash_account(CashAccountCreate(user_id=current_user.id))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.get("/me", response_model=list[CashAccountGet])
async def get_my_cash_accounts(
        current_user=Depends(require_current_user),
        service: CashAccountService = Depends(get_cash_account_service)):
    return await service.get_cash_accounts_by_user_id(current_user.id)


@router.get("/{user_id}", response_model=list[CashAccountGet])
@require_roles([RoleEnum.ADMIN])
async def get_cash_accounts_by_user_id(
        user_id: int,
        current_user=Depends(require_current_user),
        service: CashAccountService = Depends(get_cash_account_service)):
    return await service.get_cash_accounts_by_user_id(user_id)
