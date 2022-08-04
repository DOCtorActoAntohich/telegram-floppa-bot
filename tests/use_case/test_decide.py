import pytest

from floppa.models import Command
from floppa.use_case import DecideUseCase, DecideUseCaseState, DecideUseCaseMode


async def execute_decide(text: str) -> DecideUseCase:
    command, args = Command.parse(text)
    assert command is not None and command.name == "decide"

    use_case = DecideUseCase(args)
    assert use_case.state == DecideUseCaseState.NotExecuted

    _ = await use_case.execute()
    assert use_case.state != DecideUseCaseState.NotExecuted

    return use_case


@pytest.mark.asyncio
async def test_decide_no_options():
    decide_nothing = await execute_decide("/decide")
    assert decide_nothing.state == DecideUseCaseState.NoOptions
    assert decide_nothing.mode == DecideUseCaseMode.Unknown
    assert decide_nothing.selected_option == ""


@pytest.mark.asyncio
async def test_decide_one_line():
    for _ in range(100):
        decide_one_line = await execute_decide("/decide one two four! five")
        assert decide_one_line.state == DecideUseCaseState.Success
        assert decide_one_line.mode == DecideUseCaseMode.OneLine
        assert decide_one_line.selected_option != ""
        assert decide_one_line.selected_option in ["one", "two", "four!", "five"]


@pytest.mark.asyncio
async def test_decide_multi_line():
    message = (
        "/decide one and only one\n"
        "two buddies\n"
        "\n"
        "\n"
        "four!!! but what for\n"
        "\n"
        "\n"
        "two bears high five"
    )
    actual_options = [
        "one and only one",
        "two buddies",
        "four!!! but what for",
        "two bears high five",
    ]
    for _ in range(100):
        decide_multi_line = await execute_decide(message)
        assert decide_multi_line.state == DecideUseCaseState.Success
        assert decide_multi_line.mode == DecideUseCaseMode.MultiLine
        assert decide_multi_line.selected_option != ""
        assert decide_multi_line.selected_option in actual_options
