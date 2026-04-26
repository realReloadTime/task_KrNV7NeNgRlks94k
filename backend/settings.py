from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = getenv("SECRET_KEY")
    REFRESH_SECRET_KEY: str = getenv("REFRESH_SECRET_KEY")
    ALGORITHM: str = getenv("ALGORITHM")
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DB_USER: str = getenv("DB_USER", "postgres")
    DB_PASSWORD: str = getenv("DB_PASSWORD", "postgres")
    DB_HOST: str = getenv("DB_HOST", "localhost")
    DB_PORT: int = int(getenv("DB_PORT", "5432"))
    DB_NAME: str = getenv("DB_NAME", "task_db")

    IS_DEBUG: bool = getenv("IS_DEBUG", False)

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
