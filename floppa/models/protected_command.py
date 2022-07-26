from floppa.models.command import ChatType, Command


class ProtectedCommand:
    start = Command(name="start", is_hidden=True)
    help = Command(name="help")

    get_number = Command(name="get_number")
    new_number = Command(name="new_number")

    yes_no = Command(name="yes_no")
    decide = Command(name="decide")
    cat = Command(name="cat")

    set_command = Command(name="set_command", chat_type=ChatType.Group)
    del_command = Command(name="del_command", chat_type=ChatType.Group)

    github = Command(name="github", is_hidden=True)

    toggle_brackets = Command(name="toggle_brackets")

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

    @classmethod
    def is_protected(cls, command: Command) -> bool:
        commands = cls.__extract_all()
        for protected_command in commands:
            if command == protected_command:
                return True
        return False
