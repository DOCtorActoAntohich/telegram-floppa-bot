from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from pymotyc import Engine as PymotycEngine, Collection  # type: ignore

from floppa.models import Chat
from floppa.settings import Settings


pymotyc_engine = PymotycEngine()


@pymotyc_engine.database
class Storage:
    chats: Collection[Chat] = Collection(identity="chat_id")


async def connect_to_database():
    motor = AsyncIOMotorClient(Settings.mongo.connection_url)
    await pymotyc_engine.bind(motor=motor, inject_motyc_fields=True)
