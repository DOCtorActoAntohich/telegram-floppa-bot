import pymotyc  # type: ignore

from floppa.models import Chat
from floppa.storage import Storage
from floppa.repository.base import MongoRepository


class ChatRepository(MongoRepository[Chat, int]):
    @classmethod
    def create(cls):
        return cls(Storage.chats)

    def __init__(self, collection: pymotyc.Collection[Chat]):
        super().__init__(collection)

    def identity_field(self, /):
        return Chat.chat_id
