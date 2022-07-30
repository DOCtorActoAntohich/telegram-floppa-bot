from aiogram.types import Message  # type: ignore

from floppa.models import ChatType, Command
from floppa.telegram import floppa_bot
from floppa.use_case import ExecuteCustomCommandUseCase
from floppa.telegram.utils import message_chat_type


@floppa_bot.dispatcher.message_handler()
async def handle_general_message(message: Message) -> None:
    use_case = custom_command_use_case(message)
    if use_case is not None:
        await execute_custom_command(message, use_case)
        return


def custom_command_use_case(message: Message) -> ExecuteCustomCommandUseCase | None:
    if message_chat_type(message) != ChatType.Group:
        return None

    command = Command(name=message.text)
    if Command.is_malformed(command.name):
        return None

    return ExecuteCustomCommandUseCase(command, message.chat.id)


async def execute_custom_command(
    message: Message, use_case: ExecuteCustomCommandUseCase
) -> None:
    response = await use_case.execute()
    if response is None:
        return
    await message.reply(response)
