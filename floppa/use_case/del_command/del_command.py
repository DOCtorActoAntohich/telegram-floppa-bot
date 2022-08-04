from floppa.models import Chat, Command, ProtectedCommand
from floppa.repository import ChatRepository
from floppa.use_case.del_command.responses import DeleteCommandResponse
from floppa.use_case.del_command.states import DeleteCommandUseCaseState


def _extract_command(text: str | None) -> str | None:
    if text is None:
        return None
    return text.split(" ", maxsplit=1)[0]


class DeleteCommandUseCase:
    def __init__(self, text: str | None, chat_id: int) -> None:
        self.state = DeleteCommandUseCaseState.NotExecuted

        self.chats = ChatRepository.create()
        self.chat_id = chat_id

        self.command_name = _extract_command(text)

    async def execute(self) -> str:
        if self.command_name is None:
            self.state = DeleteCommandUseCaseState.NoCommandProvided
            return DeleteCommandResponse.no_command_provided()

        command = Command(name=self.command_name)
        if command.is_malformed():
            self.state = DeleteCommandUseCaseState.MalformedCommand
            return DeleteCommandResponse.malformed_command()

        if ProtectedCommand.is_protected(command):
            self.state = DeleteCommandUseCaseState.BuiltinDelete
            return DeleteCommandResponse.builtin_command_delete(command)

        chat = await self.chats.get(self.chat_id)
        if chat is None:
            chat = await self.chats.save(Chat(chat_id=self.chat_id))

        try:
            chat.commands.delete(command)
        except KeyError:
            self.state = DeleteCommandUseCaseState.CommandNotFound
            return DeleteCommandResponse.no_such_command()
        finally:
            await self.chats.update(chat)

        self.state = DeleteCommandUseCaseState.Success
        return DeleteCommandResponse.command_deleted()
