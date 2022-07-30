from __future__ import annotations

from pydantic import BaseModel, Field

from floppa.models.command import Command


class CustomCommand(BaseModel):
    command: Command = Field(...)
    response: str = Field(...)

    @property
    def name(self) -> str:
        return self.command.name

    def __str__(self):
        return f"{self.command.formatted}={{{self.response}}}"

    def same_as(self, other_command: Command) -> bool:
        return self.command == other_command


class CustomCommandsList(BaseModel):
    custom_commands: list[CustomCommand] = Field(default_factory=list)

    def __str__(self):
        commands = "\n".join("--> " + str(command) for command in self.custom_commands)
        if len(commands) == 0:
            return "[]"
        return f"[\n{commands}\n]"

    def get_response(self, command: Command) -> str:
        index = self.index_of(command)
        if index is None:
            raise KeyError(f"No such command: {command.name}")

        return self.custom_commands[index].response

    def set(self, command: Command, response: str) -> None:
        index = self.index_of(command)
        if index is not None:
            self.custom_commands[index].response = response
            return

        self.custom_commands.append(CustomCommand(command=command, response=response))

    def delete(self, command: Command) -> None:
        index = self.index_of(command)
        if index is None:
            raise KeyError(f"No such command: {command.name}")

        self.custom_commands.pop(index)

    def index_of(self, command: Command) -> int | None:
        for i, stored_command in enumerate(self.custom_commands):
            if stored_command.same_as(command):
                return i
        return None

    def exists(self, command: Command) -> bool:
        return self.index_of(command) is not None

    def all(self) -> list[Command]:
        return [c.command for c in self.custom_commands]
