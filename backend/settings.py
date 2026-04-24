from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = getenv("SECRET_KEY")
    REFRESH_SECRET_KEY: str = getenv("REFRESH_SECRET_KEY")
    ALGORITHM: str = getenv("ALGORITHM")
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = getenv("DATABASE_URL")

    IS_DEBUG: bool = getenv("IS_DEBUG", False)


settings = Settings()
