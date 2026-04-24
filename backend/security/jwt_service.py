from datetime import datetime, timedelta, UTC
from typing import Any

from jose import JWTError, jwt, ExpiredSignatureError

from backend.settings import settings


class JWTService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.refresh_secret_key = settings.REFRESH_SECRET_KEY
        self.algorithm = settings.ALGORITHM

    def create_access_token(self, data: dict[str, Any]) -> str:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self._create_token(data, expires_delta, self.secret_key)

    def create_refresh_token(self, data: dict[str, Any]) -> str:
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        data_with_type = {**data, "type": "refresh"}
        return self._create_token(data_with_type, expires_delta, self.refresh_secret_key)

    def decode_access_token(self, token: str) -> dict[str, Any]:
        return self._decode_token(token, self.secret_key)

    def decode_refresh_token(self, token: str) -> dict[str, Any]:
        payload = self._decode_token(token, self.refresh_secret_key)
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")
        return payload

    def create_code_token(self, code: int) -> str:
        expires_delta = timedelta(minutes=settings.CODE_TOKEN_EXPIRE_MINUTES)
        return self._create_token({"code": code, "type": "swap_code"}, expires_delta, self.secret_key)

    def decode_code_token(self, token: str) -> int:
        payload = self._decode_token(token, self.secret_key)
        if payload.get("type") != "swap_code":
            raise ValueError("Invalid token type")
        code = payload.get("code")
        if code is None:
            raise ValueError("Invalid token payload")
        return int(code)

    def _create_token(self, data: dict[str, Any], expires_delta: timedelta, secret_key: str) -> str:
        expire = datetime.now(UTC) + expires_delta
        to_encode = data.copy()
        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            secret_key,
            algorithm=self.algorithm
        )

    def _decode_token(self, token: str, secret_key: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except ExpiredSignatureError:
            raise ValueError("Token has expired")
        except JWTError:
            raise ValueError("Invalid token")


def get_jwt_service() -> JWTService:
    return JWTService()
