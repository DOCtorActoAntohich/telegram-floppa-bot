from floppa.models.command import Command
from floppa.settings import Settings


def test_trim_slash_and_alias():
    command = Command(name=f"/Start{Settings.bot.alias}")
    assert command.name == "start", (
        "Have to trim slash if starts with `/` and "
        "trim everything after bot alias inclusively. "
        "Have to convert to lower case after trimming."
    )


def test_trim_slash():
    command = Command(name="/sTop")
    assert command.name == "stop", (
        "Have to trim slash if starts with '/'. "
        "Have to convert to lower case after trimming"
    )


def test_trim_alias():
    command = Command(name=f"command{Settings.bot.alias}")
    assert (
        command.name == "command"
    ), "Have to trim everything after bot alias inclusively"


def test_no_trim_wrong_alias():
    command = Command(name="sus@amogus")
    assert command.name == "sus@amogus", (
        "The command should be left unchanged "
        "when it's followed by someone else's alias. "
        "Have to convert to lower case after trimming"
    )


def test_no_trim_starts_with_trash():
    command = Command(name="Updated /start")
    assert command.name == "updated /start", (
        "The command should be left unchanged " "when it doesn't start with `/`"
    )


def test_leave_beginning_trim_end():
    command = Command(name=f"You can use /kill{Settings.bot.alias} command!!")
    assert command.name == "you can use /kill", (
        "The command should always trim everything after "
        "the bot alias, but not touch anything else "
        "when it doesn't start with `/`. "
        "Have to convert to lower case after trimming"
    )


def test_trim_beginning_leave_end():
    command = Command(name="/set_command@wrong_bot command response")
    assert command.name == "set_command@wrong_bot command response", (
        "Have to trim slash if starts with '/' "
        "but not touch anything else if there's no bot alias"
    )


def test_trim_beginning_trim_end():
    command = Command(name=f"/del_command{Settings.bot.alias} bad_command")
    assert command.name == "del_command", (
        "Have to trim slash if starts with '/', and "
        "everything after bot alias inclusively"
    )


def test_lower_case_and_full_trim():
    command = Command(name=f"/DECIDE{Settings.bot.alias.upper()}")
    assert command.name == "decide", (
        "Have to trim slash if starts with '/', and "
        "everything after bot alias inclusively. "
        "Have to convert to lower case after trimming"
    )
