from backend.schemas.token import TokenPair
from backend.security.jwt_service import JWTService, get_jwt_service
from backend.services.user import UserService, get_user_service


class AuthService:
    def __init__(self, jwt_service: JWTService, user_service: UserService):
        self.jwt_service = jwt_service
        self.user_service = user_service

    async def authenticate_user(self, email: str, password: str) -> TokenPair:
        """Аутентификация пользователя"""
        user = await self.user_service.verify_user_credentials(email, password)
        if not user:
            raise ValueError("Invalid email or password")

        await self.user_service.update_last_login(user.id)
        return self.create_token_pair(user.email)

    def create_token_pair(self, email: str) -> TokenPair:
        """Создание пары токенов"""
        return TokenPair(
            access_token=self.jwt_service.create_access_token({"sub": email}),
            refresh_token=self.jwt_service.create_refresh_token({"sub": email}),
            token_type="bearer"
        )

    def create_code_token(self, code: int) -> str:
        return self.jwt_service.create_code_token(code)

    def decode_code_token(self, token: str) -> int:
        return self.jwt_service.decode_code_token(token)

    async def refresh_tokens(self, refresh_token: str) -> TokenPair:
        """Обновление токенов"""
        payload = self.jwt_service.decode_refresh_token(refresh_token)
        email = payload.get("sub")

        if not email:
            raise ValueError("Invalid refresh token")

        # Проверяем, что пользователь существует
        user = await self.user_service.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")

        return self.create_token_pair(email)


async def get_auth_service() -> AuthService:
    return AuthService(get_jwt_service(), await get_user_service())
