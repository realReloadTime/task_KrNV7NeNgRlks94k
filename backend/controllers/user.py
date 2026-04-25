from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from backend.database.enums import RoleEnum

from backend.schemas.token import TokenPair
from backend.schemas.user import UserRegister, UserUpdate, UserGet, UserCreate

from backend.security.authorization import require_current_user, refresh_token_scheme, get_current_user, require_roles
from backend.services.user import get_user_service, UserService
from backend.security.auth_service import AuthService, get_auth_service

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserGet)
async def register(
        user_data: UserRegister,
        service: UserService = Depends(get_user_service)):
    try:
        return await service.create_user(user_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    except AttributeError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )


@router.post("/login", response_model=TokenPair)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(get_auth_service)):
    try:
        return await auth_service.authenticate_user(form_data.username, form_data.password)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )


@router.post("/refresh", response_model=TokenPair)
async def refresh_tokens(
        refresh_token: str = Depends(refresh_token_scheme),
        auth_service: AuthService = Depends(get_auth_service)):
    try:
        return await auth_service.refresh_tokens(refresh_token)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )


@router.get("/me", response_model=UserGet)
async def get_me(current_user=Depends(require_current_user)):
    return UserGet.model_validate(current_user)


@require_roles([RoleEnum.ADMIN])
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserGet)
async def create_user(
        user_data: UserRegister,
        current_user=Depends(require_current_user),
        service: UserService = Depends(get_user_service)):
    try:
        return await service.create_user(user_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    except AttributeError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )


@require_roles([RoleEnum.ADMIN])
@router.put("/{user_id}", response_model=UserGet)
async def update_user(
        user_id: int,
        user_data: UserUpdate,
        current_user=Depends(require_current_user),
        service: UserService = Depends(get_user_service)):
    try:
        return await service.update_user(user_id, user_data)
    except AttributeError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@require_roles([RoleEnum.ADMIN])
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        current_user=Depends(require_current_user),
        service: UserService = Depends(get_user_service)):
    try:
        return await service.delete_user(user_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
