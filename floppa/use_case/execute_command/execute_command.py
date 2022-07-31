from floppa.models import Command
from floppa.repository import ChatRepository


class ExecuteCustomCommandUseCase:
    def __init__(self, command: Command, chat_id: int):
        self.chat_id = chat_id
        self.command = command
        self.chats = ChatRepository.create()

    async def execute(self) -> str | None:
        chat = await self.chats.get(self.chat_id)
        try:
            response = chat.commands.get_response(self.command)
        except KeyError:
            response = None

        return response
