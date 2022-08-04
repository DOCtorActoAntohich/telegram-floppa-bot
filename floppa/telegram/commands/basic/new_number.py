from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.use_case import NewNumberUseCase


@floppa_bot.dispatcher.message_handler(ProtectedCommand.new_number.filter)
async def new_number(message: Message) -> None:
    use_case = NewNumberUseCase(message.from_user.id)
    response = await use_case.execute()
    await message.reply(response)
