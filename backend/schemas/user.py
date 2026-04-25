from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from backend.database.enums import RoleEnum


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str

    surname: str
    name: str
    patronymic: str | None = None

    @field_validator('password_confirm')
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class UserCreate(BaseModel):
    email: EmailStr
    password_hash: str

    surname: str
    name: str
    patronymic: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: EmailStr | None = None

    surname: str | None = None
    name: str | None = None
    patronymic: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserGet(BaseModel):
    id: int
    full_name: str

    email: EmailStr

    surname: str
    name: str
    patronymic: str | None = None

    role: RoleEnum
    last_login: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
