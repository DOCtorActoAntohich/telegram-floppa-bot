from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from pymotyc import Engine as PymotycEngine, Collection  # type: ignore

from floppa.models import Chat, User
from floppa.settings import Settings


pymotyc_engine = PymotycEngine()


@pymotyc_engine.database
class Storage:
    chats: Collection[Chat] = Collection(identity="chat_id")
    users: Collection[User] = Collection(identity="user_id")

    @classmethod
    async def bind_to_database(cls):
        if cls.__connected:
            return
        motor = AsyncIOMotorClient(Settings.mongo.connection_url)
        await pymotyc_engine.bind(motor=motor, inject_motyc_fields=True)
        cls.__connected = True

    __connected = False
