from floppa.models import Command, CustomCommandsList


def test_collection():
    commands = CustomCommandsList()

    assert commands.index_of(Command(name="non_existent")) is None

    assert not commands.exists(Command(name="exist"))

    commands.set(Command(name="exist"), "why do I have to exist")
    assert commands.index_of(Command(name="exist")) is 0
    assert commands.exists(Command(name="exist"))

    commands.set(Command(name="one"), "1")
    commands.set(Command(name="two"), "2")
    commands.set(Command(name="three"), "3")

    assert commands.index_of(Command(name="three")) == 3
    assert commands.index_of(Command(name="two")) == 2
    assert commands.index_of(Command(name="one")) == 1

    assert commands.get_response(Command(name="one")) == "1"
    assert commands.get_response(Command(name="two")) == "2"
    assert commands.get_response(Command(name="three")) == "3"
    assert commands.get_response(Command(name="exist")) == "why do I have to exist"

    commands.set(Command(name="exist"), "existing is fun, hehe")
    assert commands.get_response(Command(name="one")) == "1"
    assert commands.get_response(Command(name="two")) == "2"
    assert commands.get_response(Command(name="three")) == "3"
    assert commands.get_response(Command(name="exist")) == "existing is fun, hehe"

    assert commands.index_of(Command(name="fake")) is None
    assert commands.index_of(Command(name="exist")) == 0
    assert commands.index_of(Command(name="one")) == 1
    assert commands.index_of(Command(name="two")) == 2
    assert commands.index_of(Command(name="three")) == 3

    assert not commands.exists(Command(name="beyond"))
    assert commands.exists(Command(name="exist"))
    assert commands.exists(Command(name="one"))
    assert commands.exists(Command(name="two"))
    assert commands.exists(Command(name="three"))

    try:
        commands.delete(Command(name="crash"))
        assert False
    except KeyError:
        pass  # lol this unironically fits, like test PASSED.

    commands.delete(Command(name="two"))

    assert not commands.exists(Command(name="two"))
    assert commands.exists(Command(name="exist"))
    assert commands.exists(Command(name="one"))
    assert commands.exists(Command(name="three"))

    assert commands.index_of(Command(name="exist")) == 0
    assert commands.index_of(Command(name="one")) == 1
    assert commands.index_of(Command(name="two")) is None
    assert commands.index_of(Command(name="three")) == 2

    assert commands.get_response(Command(name="exist")) == "existing is fun, hehe"
    assert commands.get_response(Command(name="one")) == "1"
    assert commands.get_response(Command(name="three")) == "3"

    try:
        _ = commands.get_response(Command(name="two"))
        assert False
    except KeyError:
        pass
