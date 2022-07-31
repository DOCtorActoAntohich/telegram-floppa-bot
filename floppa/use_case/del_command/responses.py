from floppa.models import Command


class DeleteCommandResponse:
    @classmethod
    def no_command_provided(cls) -> str:
        return f"Come on, how do I delete air??"

    @classmethod
    def malformed_command(cls) -> str:
        return "You messed up the command name, my friend"

    @classmethod
    def builtin_command_delete(cls, command: Command) -> str:
        return (
            f"Successfully deleted BUILT-IN command{command.formatted}.\n"
            f"Forever.\n"
            f"For good.\n\n"
            f"(jk lol, you can't)"
        )

    @classmethod
    def no_such_command(cls) -> str:
        return "No such command. You messed up, dummy"

    @classmethod
    def command_deleted(cls) -> str:
        return "Okay, done"
