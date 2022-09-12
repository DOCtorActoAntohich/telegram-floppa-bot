from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.use_case import ToggleBracketsUseCase


@floppa_bot.dispatcher.message_handler(ProtectedCommand.toggle_brackets.filter)
async def toggle_brackets(message: Message) -> None:
    use_case = ToggleBracketsUseCase(message.from_user.id)
    response = await use_case.execute()
    await message.reply(response)
