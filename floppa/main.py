import os
import signal
import logging

import aiogram

from floppa.storage import connect_to_database
from floppa.telegram import floppa_bot


def allow_insta_kill():
    # Kill destroy annihilate the container when compose down (no idea what it does).
    signal.signal(signal.SIGTERM, lambda *_: os.kill(os.getpid(), signal.SIGINT))


@floppa_bot.dispatcher.message_handler()
async def echo(message):
    await message.reply(message.text)


async def on_startup(dispatcher: aiogram.Dispatcher):
    await connect_to_database()


def main():
    floppa_bot.run(on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(
        format='(%(asctime)s) [%(name)s] [%(levelname)s] - %(message)s',
        level=logging.INFO
    )
    allow_insta_kill()
    main()
