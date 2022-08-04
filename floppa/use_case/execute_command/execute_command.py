from floppa.models import Chat, Command
from floppa.repository import ChatRepository
from floppa.use_case.execute_command.states import ExecuteCommandUseCaseState


class ExecuteCustomCommandUseCase:
    def __init__(self, command: Command, chat_id: int):
        self.state = ExecuteCommandUseCaseState.NotExecuted
        self.chat_id = chat_id
        self.command = command
        self.chats = ChatRepository.create()

    async def execute(self) -> str | None:
        chat = await self.chats.get(self.chat_id)
        if chat is None:
            chat = await self.chats.save(Chat(chat_id=self.chat_id))

        try:
            response = chat.commands.get_response(self.command)
            self.state = ExecuteCommandUseCaseState.Success
        except KeyError:
            response = None
            self.state = ExecuteCommandUseCaseState.CommandNotFound

        return response
