from aiogram.types import Message  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.telegram.commands.custom.del_command.use_case import DeleteCommandUseCase


@floppa_bot.dispatcher.message_handler(ProtectedCommand.del_command.filter)
async def delete_custom_command(message: Message) -> None:
    use_case = DeleteCommandUseCase(message.get_args(), message.chat.id)
    response = await use_case.execute()
    await message.reply(response)
