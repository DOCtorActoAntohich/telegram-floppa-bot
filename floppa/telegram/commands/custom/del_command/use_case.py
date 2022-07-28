from floppa.models import ChatType, Chat, Command, ProtectedCommand
from floppa.repository import ChatRepository
from floppa.telegram.commands.custom.del_command.responses import DeleteCommandResponse


def _extract_command(text: str | None) -> str | None:
    if text is None:
        return None
    return text.split(" ", maxsplit=1)[0]


class DeleteCommandUseCase:
    def __init__(self, text: str | None, chat_id: int) -> None:
        self.chats = ChatRepository.create()
        self.chat_id = chat_id

        self.command_name = _extract_command(text)

    async def execute(self) -> str:
        if self.command_name is None:
            return DeleteCommandResponse.no_command_provided()

        command = Command(self.command_name)
        if Command.is_malformed(command.name):
            return DeleteCommandResponse.malformed_command()

        if command in ProtectedCommand.list(chat_type=ChatType.Group):
            return DeleteCommandResponse.builtin_command_delete(command)

        chat = await self.chats.get(self.chat_id)
        if chat is None:
            chat = Chat(chat_id=self.chat_id)

        try:
            # chat.commands.pop(command)
            chat.delete_command(command)
        except KeyError:
            return DeleteCommandResponse.no_such_command()
        finally:
            await self.chats.save(chat)

        return DeleteCommandResponse.command_deleted()
