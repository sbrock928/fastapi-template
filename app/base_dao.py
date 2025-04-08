"""
Base Data Access Object (DAO) for performing async CRUD operations on SQLAlchemy models.

This module defines a generic, reusable DAO implementation intended to reduce
boilerplate across FastAPI domain layers.
"""

# pylint: disable=invalid-name

from typing import Generic, TypeVar, Type, Optional, List, Protocol, runtime_checkable

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute


@runtime_checkable
class HasId(Protocol):
    id: InstrumentedAttribute


TModel = TypeVar("TModel", bound=HasId)
TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)


class BaseDAO(Generic[TModel, TCreateSchema, TUpdateSchema]):
    """
    Abstract generic Data Access Object for performing common async CRUD operations.

    This base class reduces boilerplate by implementing typical persistence logic
    shared across domains. Subclasses are expected to provide the SQLAlchemy model class
    and appropriate Pydantic schemas for creation and update.

    Args:
        session (AsyncSession): The active database session for the DAO.
        model_class (Type[TModel]): The SQLAlchemy ORM model class this DAO handles.

    Type Parameters:
        TModel: The SQLAlchemy model class.
        TCreateSchema: The Pydantic schema used to create new model instances.
        TUpdateSchema: The Pydantic schema used to update existing model instances.
    """

    def __init__(self, session: AsyncSession, model_class: Type[TModel]):
        self.session = session
        self.model_class = model_class

    async def get(self, object_id: int) -> Optional[TModel]:
        """
        Fetch a single object by primary key.

        Args:
            object_id (int): The primary key of the object.

        Returns:
            Optional[TModel]: The object instance if found, else None.
        """
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == object_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[TModel]:
        """
        Fetch all objects of this type with optional pagination.

        Args:
            limit (int): Maximum number of records to return.
            offset (int): Number of records to skip before returning results.

        Returns:
            List[TModel]: A list of model instances.
        """
        result = await self.session.execute(select(self.model_class).offset(offset).limit(limit))
        return list(result.scalars().all())

    async def create(self, schema: TCreateSchema) -> TModel:
        """
        Insert a new object using the provided Pydantic creation schema.

        Args:
            schema (TCreateSchema): Validated creation data.

        Returns:
            TModel: The newly persisted object instance.
        """
        obj = self.model_class(**schema.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, object_id: int, schema: TUpdateSchema) -> Optional[TModel]:
        """
        Update an existing object using the provided update schema.

        Args:
            object_id (int): The primary key of the object to update.
            schema (TUpdateSchema): Partial update data.

        Returns:
            Optional[TModel]: The updated object instance, or None if not found.
        """
        obj = await self.get(object_id)
        if obj:
            for field, value in schema.model_dump(exclude_unset=True).items():
                setattr(obj, field, value)
            await self.session.commit()
            await self.session.refresh(obj)
        return obj

    async def delete(self, object_id: int) -> Optional[TModel]:
        """
        Delete an object by its primary key.

        Args:
            object_id (int): The primary key of the object to delete.

        Returns:
            Optional[TModel]: The deleted object, or None if not found.
        """
        obj = await self.get(object_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
        return obj
