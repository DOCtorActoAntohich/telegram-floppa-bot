from floppa.models import Command


def test_parse_ok():
    command, args = Command.parse("/HELP Me Win")
    assert command.name == "help", "Must be a command with args"
    assert args == "Me Win", "Must have args"


def test_parse_no_command():
    command, args = Command.parse("start the bot")
    assert command is None, "Must find no command in plain text"
    assert args is None, "Must have no args when no valid command"


def test_parse_bad_command():
    command, args = Command.parse("/am[o]gus sus imposter")
    assert command is None, "Must be None when malformed"
    assert args is None, "Must have no args when no valid command"


def test_parse_no_args():
    command, args = Command.parse("/stop")
    assert command.name == "stop", "Must be a command"
    assert args is None, "Must have no args"


def test_parse_big_space():
    command, args = Command.parse("/WhItE        sPaCe EXploRATIOn")
    assert command.name == "white", "Must be a command"
    assert args == "sPaCe EXploRATIOn", "Must have args"


def test_extract_command():
    white = Command.extract_command("/WhItE        sPaCe")
    echo = Command.extract_command("/echo")
    text = Command.extract_command("text")
    bad = Command.extract_command("/b[A]d")
    assert white.name == "white"
    assert echo.name == "echo"
    assert text is None
    assert bad is None


def test_extract_args():
    nothing = Command.extract_args("/delete")
    words = Command.extract_args("/set_command ping @everyone")
    text = Command.extract_args("plain text")
    bad = Command.extract_args("/g[oO]d command here")
    a = Command.extract_args("/c a")  # a
    assert nothing is None
    assert words == "ping @everyone"
    assert text is None
    assert bad is None
    assert a == "a"
