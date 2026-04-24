from typing import Type, TypeVar, Generic, Any
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.database.engine import get_async_session
from backend.database.models import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):  # CRUD abstract class for repositories
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, **fields) -> ModelType:
        async with get_async_session(commit=True) as session:
            try:
                instance = self.model(**fields)
                session.add(instance)
                await session.flush()
                await session.refresh(instance)
                return instance
            except IntegrityError as e:
                raise ValueError(f"Error creating {self.model.__name__}: {str(e)}")

    async def get(self, instance_id: int) -> ModelType | None:
        async with get_async_session(commit=False) as session:
            result = await session.execute(select(self.model).where(self.model.id == instance_id))
            return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        async with get_async_session(commit=False) as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def update(self, instance_id: int, **fields) -> ModelType | None:
        async with get_async_session(commit=True) as session:
            instance = await session.get(self.model, instance_id)
            if not instance:
                raise ValueError(f"{self.model.__name__} {instance_id} not found")

            for field, value in fields.items():
                setattr(instance, field, value)

            await session.flush()
            await session.refresh(instance)
            return instance

    async def delete(self, instance_id: int) -> bool:
        async with get_async_session(commit=True) as session:
            instance = await session.get(self.model, instance_id)
            if not instance:
                raise ValueError(f"{self.model.__name__} {instance_id} not found")

            await session.delete(instance)
            return True

    async def get_one_by_field(self, field_name: str, value: Any) -> ModelType | None:
        async with get_async_session(commit=False) as session:
            field = getattr(self.model, field_name)
            result = await session.execute(select(self.model).where(field == value))
            return result.scalar_one_or_none()

    async def get_by_fields_values(self, fields_values: list[tuple[str, Any]]) -> list[ModelType]:
        """ Фильтрующий метод по нескольким значениям нескольких полей. Одно поле - одно значение!

        :param fields_values: Список пар (поле, значение), например [("owner_id", UUID), ...]
        :return:
        """
        filter_line = select(self.model)
        for field, value in fields_values:
            if isinstance(value, (tuple, list, dict)):
                raise ValueError("ERROR: one field - one value!")
            column = getattr(self.model, field, None)
            if column is None:
                raise ValueError(f"Field '{field}' does not exist in model {self.model.__name__}")
            filter_line = filter_line.where(column == value)

        async with get_async_session(commit=False) as session:
            result = await session.execute(filter_line)
            return result.scalars().all()
