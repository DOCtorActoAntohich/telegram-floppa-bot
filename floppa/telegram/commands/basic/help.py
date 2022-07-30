from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.use_case import HelpUseCase
from floppa.telegram.utils import message_chat_type


@floppa_bot.dispatcher.message_handler(ProtectedCommand.help.filter)
async def help_handler(message: Message) -> None:
    chat_type = message_chat_type(message)
    use_case = HelpUseCase(chat_type, message.chat.id)
    response = await use_case.execute()
    await message.answer(response)
