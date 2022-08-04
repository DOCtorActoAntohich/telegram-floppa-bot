import pytest

from floppa.models import Command, ProtectedCommand

from floppa.use_case import (
    SetCommandUseCase,
    SetCommandUseCaseState,
    DeleteCommandUseCase,
    DeleteCommandUseCaseState,
    ExecuteCustomCommandUseCase,
    ExecuteCommandUseCaseState,
)

from floppa.storage import Storage


async def execute_set_command(text: str, chat_id: int) -> SetCommandUseCase:
    command, args = Command.parse(text)
    assert command is not None and command.formatted == "/set_command"

    use_case = SetCommandUseCase(args, chat_id)

    assert use_case.state == SetCommandUseCaseState.NotExecuted
    _ = await use_case.execute()
    assert use_case.state != SetCommandUseCaseState.NotExecuted

    return use_case


async def execute_del_command(text: str, chat_id: int) -> DeleteCommandUseCase:
    command, args = Command.parse(text)
    assert command is not None and command.formatted == "/del_command"

    use_case = DeleteCommandUseCase(args, chat_id)

    assert use_case.state == DeleteCommandUseCaseState.NotExecuted
    _ = await use_case.execute()
    assert use_case.state != DeleteCommandUseCaseState.NotExecuted

    return use_case


async def execute_custom_command(
    text: str, chat_id: int
) -> tuple[ExecuteCustomCommandUseCase, str | None]:
    command = Command.extract_command(text)
    assert command is not None

    use_case = ExecuteCustomCommandUseCase(command, chat_id)

    assert use_case.state == ExecuteCommandUseCaseState.NotExecuted
    response = await use_case.execute()
    assert use_case.state != ExecuteCommandUseCaseState.NotExecuted

    return use_case, response


@pytest.mark.parametrize("random_ids", [1], indirect=["random_ids"])
@pytest.mark.asyncio
async def test_set_command_failures(random_ids: list[int]):
    await Storage.bind_to_database()

    chat_id = random_ids[0]

    message = "/set_command"
    no_command = await execute_set_command(message, chat_id)
    assert no_command.state == SetCommandUseCaseState.NoCommand

    message = "/set_command empty"
    no_response = await execute_set_command(message, chat_id)
    assert no_response.state == SetCommandUseCaseState.NoResponse

    message = r"/set_command /o\ here's a problem!!"
    malformed = await execute_set_command(message, chat_id)
    assert malformed.state == SetCommandUseCaseState.MalformedCommand

    message = "/set_command /start /stop"
    builtin = await execute_set_command(message, chat_id)
    assert builtin.state == SetCommandUseCaseState.BuiltinOverride


@pytest.mark.parametrize("random_ids", [1], indirect=["random_ids"])
@pytest.mark.asyncio
async def test_del_command_failures(random_ids: list[int]):
    await Storage.bind_to_database()

    chat_id = random_ids[0]

    message = "/del_command"
    no_command = await execute_del_command(message, chat_id)
    assert no_command.state == DeleteCommandUseCaseState.NoCommandProvided

    message = "/del_command a[7] and 7[a] are equivalent in C++"
    malformed = await execute_del_command(message, chat_id)
    assert malformed.state == DeleteCommandUseCaseState.MalformedCommand

    message = "/del_command non_existent"
    not_found = await execute_del_command(message, chat_id)
    assert not_found.state == DeleteCommandUseCaseState.CommandNotFound

    message = "/del_command /set_command"
    builtin = await execute_del_command(message, chat_id)
    assert builtin.state == DeleteCommandUseCaseState.BuiltinDelete


@pytest.mark.parametrize("random_ids", [1], indirect=["random_ids"])
@pytest.mark.asyncio
async def test_execute_command_failures(random_ids: list[int]):
    await Storage.bind_to_database()

    chat_id = random_ids[0]

    message = "/consume"
    use_case, response = await execute_custom_command(message, chat_id)
    assert use_case.state == ExecuteCommandUseCaseState.CommandNotFound
    assert response is None


@pytest.mark.parametrize("random_ids", [2], indirect=["random_ids"])
@pytest.mark.asyncio
async def test_custom_commands(random_ids: list[int]):
    await Storage.bind_to_database()

    good_chat_id, bad_chat_id = random_ids

    one = await execute_set_command("/set_command hello hi", good_chat_id)
    two = await execute_set_command("/set_command goodbye good and bye", good_chat_id)
    assert one.state == SetCommandUseCaseState.Success
    assert two.state == SetCommandUseCaseState.Success

    one_b = await execute_set_command("/set_command hello die", bad_chat_id)
    two_b = await execute_set_command("/set_command goodbye suffer", bad_chat_id)
    assert one_b.state == SetCommandUseCaseState.Success
    assert two_b.state == SetCommandUseCaseState.Success

    one_executed, one_response = await execute_custom_command("/hello", good_chat_id)
    two_executed, two_response = await execute_custom_command("/goodbye", good_chat_id)
    one_executed_b, one_response_b = await execute_custom_command("/hello", bad_chat_id)
    two_executed_b, two_response_b = await execute_custom_command(
        "/goodbye", bad_chat_id
    )
    assert one_executed.state == ExecuteCommandUseCaseState.Success
    assert two_executed.state == ExecuteCommandUseCaseState.Success
    assert one_executed_b.state == ExecuteCommandUseCaseState.Success
    assert two_executed_b.state == ExecuteCommandUseCaseState.Success
    assert one_response == "hi"
    assert two_response == "good and bye"
    assert one_response_b == "die"
    assert two_response_b == "suffer"

    del_two = await execute_del_command("/del_command goodbye", good_chat_id)
    del_one_b = await execute_del_command("/del_command hello", bad_chat_id)
    assert del_two.state == DeleteCommandUseCaseState.Success
    assert del_one_b.state == DeleteCommandUseCaseState.Success

    one = await execute_set_command("/set_command hello friend!!", good_chat_id)
    assert one.state == SetCommandUseCaseState.Success

    one_executed, one_response = await execute_custom_command("/hello", good_chat_id)
    two_executed_b, two_response_b = await execute_custom_command(
        "/goodbye", bad_chat_id
    )
    assert one_executed.state == ExecuteCommandUseCaseState.Success
    assert two_executed_b.state == ExecuteCommandUseCaseState.Success
    assert one_response == "friend!!"
    assert two_response_b == "suffer"

    two_executed, two_response = await execute_custom_command("/goodbye", good_chat_id)
    one_executed_b, one_response_b = await execute_custom_command("/hello", bad_chat_id)
    assert two_executed.state == ExecuteCommandUseCaseState.CommandNotFound
    assert one_executed_b.state == ExecuteCommandUseCaseState.CommandNotFound
    assert two_response is None
    assert one_response_b is None
