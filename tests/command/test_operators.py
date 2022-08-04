from floppa.models import ChatType, Command
from floppa.settings import Settings


def test_equality_operator():
    left = Command(name="start", chat_type=ChatType.Group)
    middle = Command(name=f"/START", chat_type=ChatType.Any, is_hidden=True)
    right = Command(
        name=f"/start{Settings.bot.alias}", chat_type=ChatType.Private, is_hidden=True
    )
    assert left == middle == right


def test_inequality_operator():
    left = Command(name="start", chat_type=ChatType.Private, is_hidden=True)
    right = Command(name=f"stop", chat_type=ChatType.Private, is_hidden=True)
    assert left != right
