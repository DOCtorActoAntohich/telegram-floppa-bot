import aiogram.types  # type: ignore

from floppa.models import ChatType


def message_chat_type(message: aiogram.types.Message) -> ChatType:
    if message.chat.type == aiogram.types.ChatType.PRIVATE:
        return ChatType.Private
    return ChatType.Group
