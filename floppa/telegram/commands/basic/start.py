from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.use_case import StartUseCase
from floppa.telegram.utils import message_chat_type


@floppa_bot.dispatcher.message_handler(ProtectedCommand.start.filter)
async def start(message: Message) -> None:
    chat_type = message_chat_type(message)
    use_case = StartUseCase(chat_type)
    response = await use_case.execute()
    await message.answer(response)
