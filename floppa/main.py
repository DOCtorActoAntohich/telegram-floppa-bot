import os
import asyncio
import signal
import logging

from floppa.storage import Storage, WhatThe, connect_to_database


logging.basicConfig(
    format='(%(asctime)s) [%(name)s] [%(levelname)s] - %(message)s',
    level=logging.INFO
)


def allow_insta_kill():
    # Kill destroy annihilate the container when compose down (no idea what it does).
    signal.signal(signal.SIGTERM, lambda *_: os.kill(os.getpid(), signal.SIGINT))


async def main():
    await connect_to_database()
    await Storage.funny.save(WhatThe(cost=0))
    logger = logging.getLogger(__name__)
    logger.critical("IT WORKS IT WORKS ? ?! ?! ?!? ! hehe")


if __name__ == "__main__":
    allow_insta_kill()
    asyncio.run(main())
