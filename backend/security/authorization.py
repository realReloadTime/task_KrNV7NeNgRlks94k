from typing import Optional, Callable
from functools import wraps

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.database.models import User
from backend.database.enums import RoleEnum
from backend.security.jwt_service import JWTService, get_jwt_service
from backend.services.user import UserService, get_user_service

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="users/login",
    auto_error=False
)

refresh_token_scheme = OAuth2PasswordBearer(
    tokenUrl="users/refresh",
    auto_error=False
)


async def get_current_user(
        token: Optional[str] = Depends(oauth2_scheme),
        jwt_service: JWTService = Depends(get_jwt_service),
        user_service: UserService = Depends(get_user_service)
) -> Optional[User]:
    """Dependency для получения текущего пользователя (опционально)"""
    if not token:
        return None

    try:
        payload = jwt_service.decode_access_token(token)
        email = payload.get("sub")
        if not email:
            return None

        return await user_service.get_user_by_email(email)

    except ValueError as e:
        error_msg = str(e)
        if "expired" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Для невалидных токенов просто возвращаем None
        return None


async def require_current_user(
        current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """Dependency для обязательной аутентификации"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


async def get_current_user_refresh(
        token: Optional[str] = Depends(refresh_token_scheme),
        jwt_service: JWTService = Depends(get_jwt_service),
        user_service: UserService = Depends(get_user_service)
) -> User:
    """Dependency для проверки refresh токена"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required"
        )

    try:
        payload = jwt_service.decode_refresh_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user = await user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


def check_role(current_user: User, allowed_roles: list[RoleEnum]) -> bool:
    if not current_user:
        return False
    return current_user.role in allowed_roles


def require_roles(allowed_roles: list[RoleEnum]):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')

            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access is denied. Required role(s): {[r.value for r in allowed_roles]}"
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
