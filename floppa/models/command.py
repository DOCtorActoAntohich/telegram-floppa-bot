from __future__ import annotations

import re
from enum import IntEnum, auto

import aiogram  # type: ignore

from floppa.settings import Settings


# noinspection PyArgumentList
class ChatType(IntEnum):
    Any = auto()
    Private = auto()
    Group = auto()


class Command:
    def __init__(
        self,
        command: str,
        *,
        chat_type: ChatType = ChatType.Any,
        is_hidden: bool = False,
    ):
        self.name = self.extract_name(command)
        self.chat_type = chat_type
        self.is_hidden = is_hidden

    def __eq__(self, other):
        return isinstance(other, Command) and self.name == other.name

    def __ne__(self, other):
        return not isinstance(other, Command) or self.name != other.name

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_command_name

    def fits(self, chat_type: ChatType) -> bool:
        if chat_type == ChatType.Any:
            return True
        if self.chat_type == ChatType.Any:
            return True
        return self.chat_type == chat_type

    @property
    def formatted(self) -> str:
        return f"/{self.name}"

    @property
    def filter(self) -> aiogram.dispatcher.filters.Command:
        return aiogram.dispatcher.filters.Command(self.name)

    @classmethod
    def extract_name(cls, command: str) -> str:
        if command.startswith("/"):
            command = command[1:]

        alias_pos = command.find(Settings.bot.alias)
        if alias_pos >= 0:
            command = command[:alias_pos]

        return command.lower()

    @classmethod
    def regex(cls) -> str:
        return r"[a-z0-9_]+"

    @classmethod
    def is_malformed(cls, name: str) -> bool:
        return re.match(cls.regex(), name) is None

    @classmethod
    def is_valid(cls, name: str) -> bool:
        return not cls.is_malformed(name)

    @classmethod
    def validate_command_name(cls, name: str) -> str:
        if cls.is_valid(name):
            return name
        raise ValueError(f"Command name is invalid: {name}")
