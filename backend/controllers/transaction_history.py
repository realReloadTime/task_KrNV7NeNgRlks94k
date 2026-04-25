from fastapi import APIRouter, Depends, status, HTTPException

from backend.database.enums import RoleEnum

from backend.schemas.transaction_history import TransactionHistoryGet, TransactionHistoryCreate, TransactionHistoryInput

from backend.security.authorization import require_current_user, require_roles
from backend.services.transaction_history import get_transaction_history_service, TransactionHistoryService

router = APIRouter(prefix="/transaction-histories", tags=["Transaction History"])


@router.post("/webhook", response_model=TransactionHistoryGet, status_code=status.HTTP_201_CREATED)
async def create_transaction_history(
        data: TransactionHistoryInput,
        service: TransactionHistoryService = Depends(get_transaction_history_service)):
    try:
        return await service.create_transaction(data)
    except AssertionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Signature validation failed')
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.get('/me', response_model=list[TransactionHistoryGet])
async def get_transaction_history_by_me(
        current_user=Depends(require_current_user),
        service: TransactionHistoryService = Depends(get_transaction_history_service)):
    return await service.get_transaction_history_by_user_id(current_user.id)


@router.get('/by-user/{user_id}', response_model=list[TransactionHistoryGet])
@require_roles([RoleEnum.ADMIN])
async def get_transaction_history_by_user_id(
        user_id: int,
        current_user=Depends(require_current_user),
        service: TransactionHistoryService = Depends(get_transaction_history_service)):
    return await service.get_transaction_history_by_user_id(user_id)
