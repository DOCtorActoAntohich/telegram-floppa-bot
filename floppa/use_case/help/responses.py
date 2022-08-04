from floppa.models import Command


class HelpCommandResponse:
    @classmethod
    def private_chat(cls, commands: list[Command]):
        return (
            "I am smart Floppa and I can do stuff!!\n"
            "You can just experiment by tapping on some commands.\n\n"
            "Here they are:\n"
            f"{cls._list_to_str(commands)}"
        )

    @classmethod
    def group_chat(cls, commands: list[Command]):
        return "Available commands:\n" f"{cls._list_to_str(commands)}"

    @classmethod
    def _list_to_str(cls, commands: list[Command]):
        names = [command.formatted for command in commands]
        return ", ".join(sorted(names))
