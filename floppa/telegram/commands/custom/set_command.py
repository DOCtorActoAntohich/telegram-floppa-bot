from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.use_case import SetCommandUseCase


@floppa_bot.dispatcher.message_handler(ProtectedCommand.set_command.filter)
async def set_custom_command(message: Message) -> None:
    use_case = SetCommandUseCase(message.get_args(), message.chat.id)
    response = await use_case.execute()
    await message.reply(response)