from pydantic import BaseModel, Field

from floppa.models.command import Command
from floppa.models.custom_command import CustomCommand


class Chat(BaseModel):
    chat_id: int = Field(...)
    # commands: dict[Command, str] = Field(default_factory=dict)
    commands: list[CustomCommand] = Field(default_factory=list)

    def __find_index(self, command: Command) -> int | None:
        for i in range(len(self.commands)):
            if self.commands[i] == command:
                return i
        return None

    def delete_command(self, command: Command) -> None:
        it = self.__find_index(command)
        if it is None:
            raise KeyError(f"No such command: {command.name}")

        self.commands.pop(it)

    def set_command(self, command: Command, response: str) -> None:
        at = self.__find_index(command)
        if at is not None:
            self.commands[at].response = response
            return

        new = CustomCommand(command=command, response=response)
        self.commands.append(new)
