from aiogram.types import Message  # type: ignore

from floppa.models import Command, ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.telegram.command_restrictions import CommandRestriction
from floppa.use_case import DeleteCommandUseCase


@floppa_bot.dispatcher.message_handler(ProtectedCommand.del_command.filter)
@CommandRestriction.only_for_chat_admins
async def delete_custom_command(message: Message) -> None:
    args = Command.parse_args(message.text)
    use_case = DeleteCommandUseCase(args, message.chat.id)
    response = await use_case.execute()
    await message.reply(response)
