from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.use_case import YesNoUseCase


@floppa_bot.dispatcher.message_handler(ProtectedCommand.yes_no.filter)
async def yes_no(message: Message) -> None:
    use_case = YesNoUseCase()
    response = await use_case.execute()
    await message.reply(response)
