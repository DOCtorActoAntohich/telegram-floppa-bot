from aiogram.types import Message  # type: ignore

from floppa.models import Command, ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.use_case import DecideUseCase


@floppa_bot.dispatcher.message_handler(ProtectedCommand.decide.filter)
async def decide(message: Message) -> None:
    options_text = Command.parse_args(message.text)
    use_case = DecideUseCase(options_text)
    response = await use_case.execute()
    await message.reply(response)
