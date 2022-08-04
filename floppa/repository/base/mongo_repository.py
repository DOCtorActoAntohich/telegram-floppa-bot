from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar

import pymotyc  # type: ignore

from floppa.repository.base.repository_base import RepositoryBase

ASCENDING_ORDER = 1

MongoModel = TypeVar("MongoModel")
ModelIdType = TypeVar("ModelIdType")


class MongoRepository(RepositoryBase[MongoModel, ModelIdType]):
    @abstractmethod
    def __init__(self, collection: pymotyc.Collection[MongoModel]):
        self._collection: pymotyc.Collection[MongoModel] = collection

    @abstractmethod
    def identity_field(self, /):
        pass

    def _identity_query(self, identity: ModelIdType, /) -> dict:
        return {self.identity_field(): identity}

    def _sorting_query(self) -> dict:
        return {self.identity_field(): ASCENDING_ORDER}

    async def save(self, item: MongoModel, /) -> MongoModel:
        return await self._collection.save(item)

    async def exists(self, identity: ModelIdType, /) -> bool:
        try:
            _ = await self._collection.find_one(self._identity_query(identity))
        except pymotyc.errors.NotFound:
            return False
        return True

    async def get(self, identity: ModelIdType, /) -> MongoModel | None:
        try:
            return await self._collection.find_one(self._identity_query(identity))
        except pymotyc.errors.NotFound:
            return None

    async def get_all(self, /) -> list[MongoModel]:
        return await self._collection.find({}, sort=self._sorting_query())

    async def update(self, item: MongoModel, /) -> MongoModel | None:
        try:
            return await self._collection.save(item, mode="update")
        except pymotyc.errors.NotFound:
            return None

    async def delete(self, identity: ModelIdType, /) -> bool:
        try:
            await self._collection.delete_one(self._identity_query(identity))
        except pymotyc.errors.NotFound:
            return False
        return True
