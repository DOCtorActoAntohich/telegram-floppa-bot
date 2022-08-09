from __future__ import annotations

import re
from enum import IntEnum, auto

import aiogram  # type: ignore
from pydantic import BaseModel, Field

from floppa.settings import Settings


# noinspection PyArgumentList
class ChatType(IntEnum):
    Any = auto()
    Private = auto()
    Group = auto()


class Command(BaseModel):
    name: str = Field(...)
    chat_type: ChatType = Field(ChatType.Any)
    is_hidden: bool = Field(False)

    def __init__(
        self, *, name: str, chat_type: ChatType = ChatType.Any, is_hidden: bool = False
    ):
        super().__init__(
            name=self.extract_name(name), chat_type=chat_type, is_hidden=is_hidden
        )

    def __eq__(self, other):
        return isinstance(other, Command) and self.name == other.name

    def __ne__(self, other):
        return not isinstance(other, Command) or self.name != other.name

    @classmethod
    def __get_validators__(cls):
        yield from super().__get_validators__()
        yield cls.validate_command_name

    def fits(self, requested_type: ChatType) -> bool:
        if requested_type == ChatType.Any:
            return True
        if self.chat_type == ChatType.Any:
            return True
        return self.chat_type == requested_type

    @property
    def formatted(self) -> str:
        return f"/{self.name}"

    @property
    def filter(self) -> aiogram.dispatcher.filters.Command:
        return aiogram.dispatcher.filters.Command(self.name)

    def is_valid(self):
        return self.is_name_valid(self.name)

    def is_malformed(self):
        return self.is_name_malformed(self.name)

    @classmethod
    def extract_name(cls, command: str) -> str:
        command = command.lower()

        if command.startswith("/"):
            command = command[1:]

        alias_pos = command.find(Settings.bot.alias.lower())
        if alias_pos >= 0:
            command = command[:alias_pos]

        return command

    @classmethod
    def regex(cls) -> str:
        return r"^[a-z0-9_]+$"

    @classmethod
    def is_name_malformed(cls, name: str) -> bool:
        return re.match(cls.regex(), name) is None

    @classmethod
    def is_name_valid(cls, name: str) -> bool:
        return not cls.is_name_malformed(name)

    @classmethod
    def parse(cls, text: str) -> tuple[Command | None, str | None]:
        if not text.startswith("/"):
            return None, None

        command_name, *maybe_args = text.split(maxsplit=1)

        args = maybe_args[0].strip() if maybe_args else None
        if args == "":
            args = None

        command = cls(name=command_name)
        if command.is_malformed():
            return None, None

        return command, args

    @classmethod
    def parse_command(cls, text: str) -> Command | None:
        command, _ = cls.parse(text)
        return command

    @classmethod
    def parse_args(cls, text: str) -> str | None:
        command, args = cls.parse(text)
        if command is None:
            return None

        return args

    @classmethod
    def validate_command_name(cls, command: Command) -> Command:
        if command.is_valid():
            return command
        raise ValueError(f"Command name is invalid: {command.name}")
