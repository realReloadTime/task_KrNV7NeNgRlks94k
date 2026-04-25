from backend.repositories.user import UserRepository
from backend.schemas.user import UserRegister, UserUpdate, UserGet
from backend.security.password import PasswordService


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_email(self, email: str):
        """Только для repository - возвращаем модель, не схему"""
        return await self.user_repository.get_user_by_email(email)

    async def verify_user_credentials(self, email: str, password: str):
        """Проверка учетных данных пользователя для AuthService"""
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            return None
        if not PasswordService.verify_password(password, user.password_hash):
            return None
        return user

    async def create_user(self, user_data: UserRegister) -> UserGet:
        hashed_password = PasswordService.hash_password(user_data.password)
        user = await self.user_repository.create(
            email=user_data.email,
            password_hash=hashed_password,

            surname=user_data.surname,
            name=user_data.name,
            patronymic=user_data.patronymic,
        )
        schema = UserGet.model_validate(user)
        return schema

    async def update_last_login(self, user_id: int) -> None:
        await self.user_repository.user_access(user_id=user_id)

    async def get_all(self) -> list[UserGet]:
        users = await self.user_repository.get_all()
        return list(map(UserGet.model_validate, users))

    async def get_user_by_id(self, user_id: int) -> UserGet:
        user = await self.user_repository.get(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")
        return UserGet.model_validate(user)

    async def update_user(self, user_id: int, new_user_data: UserUpdate) -> UserGet:
        update_data = new_user_data.model_dump(exclude_unset=True)
        if 'email' in update_data and await self.user_repository.get_user_by_email(update_data['email']):
            raise AttributeError('Email already registered')
        updated_user = await self.user_repository.update(user_id, **update_data)
        return await UserGet.model_validate(updated_user)

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)


async def get_user_service() -> UserService:
    return UserService(UserRepository())
