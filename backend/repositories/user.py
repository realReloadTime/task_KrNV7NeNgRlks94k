from datetime import datetime, UTC

from backend.database.models import User
from backend.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.get_one_by_field('email', email)

    async def user_access(self, user_id: int) -> bool:
        user = await self.get(user_id)
        if user is None:
            raise ValueError(f'User not found: {user_id}')
        setattr(user, 'last_login', datetime.now(UTC))
        return True

    async def update_password_by_email(self, email: str, new_password_hash: str) -> User:
        user = await self.get_user_by_email(email)
        if user is None:
            raise ValueError(f'User not found: {email}')

        return await self.update(user.id, password_hash=new_password_hash)


async def get_user_repository() -> UserRepository:
    return UserRepository()
