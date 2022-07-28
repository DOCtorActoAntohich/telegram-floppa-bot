from floppa.models import Command, ProtectedCommand


class SetCommandResponse:
    @classmethod
    def no_command_provided(cls) -> str:
        return "But what command? lol"

    @classmethod
    def no_response_provided(cls, new_name: str) -> str:
        return (
            "You should've told me how to respond to your command.\n"
            "Like this, check this out:\n"
            f"`{ProtectedCommand.set_command.formatted} {new_name or '<command>'} <response>`"
        )

    @classmethod
    def malformed_command(cls) -> str:
        return (
            "Wtf is that command? Me no understand.\n"
            "Pls only latin letters, underscores, maybe numbers..."
        )

    @classmethod
    def builtin_command_override(cls):
        return "Cannot override built-in commands, dummy!!"

    @classmethod
    def command_updated(cls, new_command: Command) -> str:
        return f"Updated {new_command.formatted} for you"
