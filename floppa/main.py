import os
import signal
import logging

import aiogram  # type: ignore

from floppa.storage import connect_to_database
from floppa.telegram import floppa_bot


def allow_insta_kill() -> None:
    # Kill destroy annihilate the container when compose down (no idea what it does).
    signal.signal(signal.SIGTERM, lambda *_: os.kill(os.getpid(), signal.SIGINT))


async def on_startup(dispatcher: aiogram.Dispatcher) -> None:
    await connect_to_database()


def main() -> None:
    floppa_bot.run(on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(
        format="(%(asctime)s) [%(name)s] [%(levelname)s] - %(message)s",
        level=logging.INFO,
    )
    allow_insta_kill()
    main()
