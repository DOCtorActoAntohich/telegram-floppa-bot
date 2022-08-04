from floppa.models import ChatType, Chat, ProtectedCommand
from floppa.repository import ChatRepository
from floppa.use_case.help.responses import HelpCommandResponse


class HelpUseCase:
    def __init__(self, chat_type: ChatType, chat_id: int) -> None:
        self.chats = ChatRepository.create()
        self.chat_type = chat_type
        self.chat_id = chat_id

    async def execute(self) -> str:
        if self.chat_type == ChatType.Private:
            return await self._response_to_pms()
        return await self._response_to_groups()

    @classmethod
    async def _response_to_pms(cls) -> str:
        commands = ProtectedCommand.list(chat_type=ChatType.Private)
        return HelpCommandResponse.private_chat(commands)

    async def _response_to_groups(self) -> str:
        chat = await self.chats.get(self.chat_id)
        if chat is None:
            chat = await self.chats.save(Chat(chat_id=self.chat_id))

        commands = ProtectedCommand.list(chat_type=ChatType.Group)
        commands.extend(chat.commands.all())
        return HelpCommandResponse.group_chat(commands)
