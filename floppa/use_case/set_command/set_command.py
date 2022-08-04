from floppa.models import ChatType, Chat, Command, ProtectedCommand
from floppa.repository import ChatRepository
from floppa.use_case.set_command.responses import SetCommandResponse
from floppa.use_case.set_command.states import SetCommandUseCaseState


class SetCommandUseCase:
    def __init__(self, text: str | None, chat_id: int) -> None:
        self.state = SetCommandUseCaseState.NotExecuted

        self.chats = ChatRepository.create()
        self.chat_id = chat_id

        self.command: str | None
        self.command_response: str | None

        if text is None or text == "":
            self.command, self.command_response = None, None
            return

        args = text.split(" ", maxsplit=1)
        try:
            self.command, self.command_response = args
        except ValueError:
            self.command, self.command_response = args[0], None

    async def execute(self) -> str:
        if self.command is None:
            self.state = SetCommandUseCaseState.NoCommand
            return SetCommandResponse.no_command_provided()

        if self.command_response is None:
            self.state = SetCommandUseCaseState.NoResponse
            return SetCommandResponse.no_response_provided(self.command)

        new_command = Command(name=self.command)
        if new_command.is_malformed():
            self.state = SetCommandUseCaseState.MalformedCommand
            return SetCommandResponse.malformed_command()

        if ProtectedCommand.is_protected(new_command):
            self.state = SetCommandUseCaseState.BuiltinOverride
            return SetCommandResponse.builtin_command_override()

        chat = await self.chats.get(self.chat_id)
        if chat is None:
            chat = await self.chats.save(Chat(chat_id=self.chat_id))

        chat.commands.set(new_command, self.command_response)
        await self.chats.update(chat)

        self.state = SetCommandUseCaseState.Success
        return SetCommandResponse.command_updated(new_command)
