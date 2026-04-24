from sqlalchemy import ForeignKey, func, DateTime, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from backend.database.engine import uniq_str, Base
from backend.database.enums import RoleEnum


class User(Base):
    surname: Mapped[str]
    name: Mapped[str]
    patronymic: Mapped[str | None]

    email: Mapped[str]
    password_hash: Mapped[str]

    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.USER)

    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    cash_accounts = relationship('CashAccount', backref='user', cascade='all, delete-orphan', lazy='selectin')

    @property
    def full_name(self) -> str:
        return f'{self.surname} {self.name} {self.patronymic if self.patronymic is not None else ""}'.strip()


class CashAccount(Base):
    __tablename__ = 'cash_accounts'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    balance: Mapped[float] = mapped_column(Float, default=0)

    user = relationship('User', backref='cash_accounts', uselist=False)
    transactions = relationship('TransactionHistory', backref='cash_account', cascade='all, delete-orphan',
                                lazy='selectin')


class TransactionHistory(Base):
    __tablename__ = 'transaction_histories'

    cash_account_id: Mapped[int] = mapped_column(ForeignKey('cash_accounts.id'))
    side_transaction_id: Mapped[uniq_str]

    amount: Mapped[Float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    cash_account = relationship('CashAccount', backref='transactions', uselist=False)
