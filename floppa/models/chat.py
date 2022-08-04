from pydantic import BaseModel, Field

from floppa.models.custom_command import CustomCommandsList


class Chat(BaseModel):
    chat_id: int = Field(...)
    commands: CustomCommandsList = Field(default_factory=CustomCommandsList)
