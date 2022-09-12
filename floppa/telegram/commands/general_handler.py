from aiogram.types import Message  # type: ignore

from floppa.models import ChatType, Command
from floppa.telegram import floppa_bot
from floppa.telegram.utils import message_chat_type
from floppa.use_case import (
    ExecuteCustomCommandUseCase,
    RegexKeywordSearchUseCase,
    ValidateBracketsUseCase,
)


@floppa_bot.dispatcher.message_handler()
async def handle_general_message(message: Message) -> None:
    command_use_case = custom_command_use_case(message)
    if command_use_case is not None:
        await execute_custom_command(message, command_use_case)
        return

    animation_use_case = RegexKeywordSearchUseCase(message.text)
    link = await animation_use_case.execute()
    if link is not None:
        await message.reply_animation(link)
        return

    brackets_use_case = ValidateBracketsUseCase(message.from_user.id, message.text)
    response = await brackets_use_case.execute()
    if response is not None:
        await message.reply(response)


def custom_command_use_case(message: Message) -> ExecuteCustomCommandUseCase | None:
    if message_chat_type(message) != ChatType.Group:
        return None

    command = Command.parse_command(message.text)
    if command is None or command.is_malformed():
        return None

    return ExecuteCustomCommandUseCase(command, message.chat.id)


async def execute_custom_command(
    message: Message, use_case: ExecuteCustomCommandUseCase
) -> None:
    response = await use_case.execute()
    if response is None:
        return
    await message.reply(response)
