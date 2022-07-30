from floppa.models import ChatType

from floppa.use_case.start.responses import StartCommandResponse


class StartUseCase:
    def __init__(self, chat_type: ChatType):
        self.chat_type = chat_type

    async def execute(self) -> str:
        if self.chat_type == ChatType.Private:
            return StartCommandResponse.private_chat()
        return StartCommandResponse.group_chat()
