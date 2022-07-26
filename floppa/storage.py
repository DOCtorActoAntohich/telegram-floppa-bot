from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from pymotyc import Engine as PymotycEngine, Collection

from floppa.settings import Settings


pymotyc_engine = PymotycEngine()


class WhatThe(BaseModel):
    cost: int


@pymotyc_engine.database
class Storage:
    funny: Collection[WhatThe] = Collection()


async def connect_to_database():
    motor = AsyncIOMotorClient(Settings.mongo.connection_url)
    await pymotyc_engine.bind(motor=motor, inject_motyc_fields=True)
