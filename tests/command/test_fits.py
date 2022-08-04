from floppa.models import ChatType, Command


def test_bruteforce():
    chat_any = Command(name="any", chat_type=ChatType.Any)
    chat_group = Command(name="group", chat_type=ChatType.Group)
    chat_private = Command(name="private", chat_type=ChatType.Private)

    assert chat_any.fits(ChatType.Any)
    assert chat_any.fits(ChatType.Group)
    assert chat_any.fits(ChatType.Private)

    assert chat_group.fits(ChatType.Any)
    assert chat_group.fits(ChatType.Group)
    assert not chat_group.fits(ChatType.Private)

    assert chat_private.fits(ChatType.Any)
    assert not chat_private.fits(ChatType.Group)
    assert chat_private.fits(ChatType.Private)
