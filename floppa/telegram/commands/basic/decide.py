from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.use_case import DecideUseCase


@floppa_bot.dispatcher.message_handler(ProtectedCommand.decide.filter)
async def decide(message: Message) -> None:
    use_case = DecideUseCase(message.get_args())
    response = await use_case.execute()
    await message.reply(response)
