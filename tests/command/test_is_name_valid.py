from floppa.models import Command
from floppa.settings import Settings


def test_valid_names():
    valid_names = [
        "_",
        "___________",
        "1",
        "a",
        "help",
        "he5p",
        "break_armor",
        "break_armor________________________0",
        "_ki11",
    ]
    for name in valid_names:
        assert Command.is_valid(name), (
            f"Command name `{name}` should be Valid. "
            "All commands should consist of small latin letters, "
            "numbers, and underscores"
        )


def test_invalid_names():
    invalid_names = [
        "A_B_C",
        "help me",
        "Kill",
        "_ _",
        "Did you know that, unfortunately, you cannot do that?",
        "",
        " ",
        "/kill",
        f"/kill{Settings}",
    ]
    for name in invalid_names:
        assert Command.is_malformed(name), (
            f"Command name `{name}` should be Invalid. "
            "All commands should consist of small latin letters, "
            "numbers, and underscores"
        )
