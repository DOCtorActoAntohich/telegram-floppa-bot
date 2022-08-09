from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot


@floppa_bot.dispatcher.message_handler(ProtectedCommand.github.filter)
async def github(message: Message) -> None:
    await message.reply(
        "This is my source code:\n"
        "https://github.com/DOCtorActoAntohich/telegram-floppa-bot\n\n"
        "You can contribute to this repository!\n"
        "And maybe suggest features or report bugs by creating a new issue.\n\n"
        "Let's make flop have no issue!"
    )
