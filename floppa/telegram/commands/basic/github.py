from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot


@floppa_bot.dispatcher.message_handler(ProtectedCommand.github.filter)
async def github(message: Message) -> None:
    await message.reply(
        "This is my source code:\n"
        "https://github.com/DOCtorActoAntohich/telegram-floppa-bot"
    )
