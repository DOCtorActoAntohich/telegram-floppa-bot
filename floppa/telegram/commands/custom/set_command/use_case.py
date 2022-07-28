from floppa.models import ChatType, Chat, Command, ProtectedCommand
from floppa.repository import ChatRepository
from floppa.telegram.commands.custom.set_command.responses import SetCommandResponse


class SetCommandUseCase:
    def __init__(self, text: str | None, chat_id: int) -> None:
        self.chats = ChatRepository.create()
        self.chat_id = chat_id

        self.command: str | None
        self.command_response: str | None

        if text is None:
            self.command, self.command_response = None, None
            return

        args = text.split(" ", maxsplit=1)
        try:
            self.command, self.command_response = args
        except ValueError:
            self.command, self.command_response = args[0], None

    async def execute(self) -> str:
        if self.command is None:
            return SetCommandResponse.no_command_provided()

        if self.command_response is None:
            return SetCommandResponse.no_response_provided(self.command)

        new_command = Command(self.command)
        if Command.is_malformed(new_command.name):
            return SetCommandResponse.malformed_command()

        if new_command in ProtectedCommand.list(chat_type=ChatType.Group):
            return SetCommandResponse.builtin_command_override()

        chat = await self.chats.get(self.chat_id)
        if chat is None:
            chat = Chat(chat_id=self.chat_id)
        # chat.commands[new_command] = self.command_response
        chat.set_command(new_command, self.command_response)
        await self.chats.save(chat)

        return SetCommandResponse.command_updated(new_command)
