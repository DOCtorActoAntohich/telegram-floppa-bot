from pydantic import BaseModel, Field

from floppa.models.command import Command


class CustomCommand(BaseModel):
    command: Command = Field(...)
    response: str = Field(...)

    @property
    def name(self) -> str:
        return self.command.name

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_command
        yield cls.validate_response

    @classmethod
    def validate_command(cls, command: Command) -> Command:
        Command.validate_command_name(command.name)
        return command

    @classmethod
    def validate_response(cls, response: str) -> str:
        if len(response) == 0:
            raise ValueError("Response cannot be empty")
        return response
