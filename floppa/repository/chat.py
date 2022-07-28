import pymotyc  # type: ignore

from floppa.models import Chat
from floppa.storage import Storage


ASCENDING_ORDER = 1


class ChatRepository:
    @classmethod
    def create(cls):
        return cls(Storage.chats)

    def __init__(self, collection: pymotyc.Collection[Chat]):
        self.collection: pymotyc.Collection[Chat] = collection

    async def save(self, chat: Chat) -> Chat:
        return await self.collection.save(chat, mode="update")

    async def exists(self, chat_id: int) -> bool:
        try:
            _ = await self.collection.find_one({Chat.chat_id: chat_id})
        except pymotyc.errors.NotFound:
            return False
        return True

    async def get(self, chat_id: int) -> Chat | None:
        try:
            return await self.collection.find_one({Chat.chat_id: chat_id})
        except pymotyc.errors.NotFound:
            return None

    async def get_all(self) -> list[Chat]:
        return await self.collection.find({}, sort={Chat.chat_id: ASCENDING_ORDER})

    async def delete(self, chat_id: int) -> bool:
        try:
            await self.collection.delete_one({Chat.chat_id: chat_id})
        except pymotyc.errors.NotFound:
            return False
        return True
