from floppa.models.command import ChatType, Command


class ProtectedCommand:
    start = Command("start", is_hidden=True)
    help = Command("help")

    set_command = Command("set_command", chat_type=ChatType.Group)
    del_command = Command("del_command", chat_type=ChatType.Group)

    @classmethod
    def __extract_all(cls) -> list[Command]:
        return [
            value
            for member, value in cls.__dict__.items()
            if not member.startswith("_") and isinstance(value, Command)
        ]

    @classmethod
    def list(cls, chat_type: ChatType) -> list[Command]:
        return [
            command
            for command in cls.__extract_all()
            if command.fits(chat_type) and not command.is_hidden
        ]
