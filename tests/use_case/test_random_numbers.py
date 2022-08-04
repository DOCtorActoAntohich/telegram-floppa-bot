import pytest

from floppa.repository import UserRepository
from floppa.storage import Storage
from floppa.use_case import GetNumberUseCase, NewNumberUseCase


@pytest.mark.parametrize("random_ids", [1], indirect=["random_ids"])
@pytest.mark.asyncio
async def test_random_numbers(random_ids: list[int]):
    await Storage.bind_to_database()
    users = UserRepository.create()

    user_id = random_ids[0]

    user = await users.get(user_id)
    assert user is None

    get_number_fail = GetNumberUseCase(user_id)
    assert get_number_fail.random_number is None
    _ = await get_number_fail.execute()
    assert get_number_fail.random_number is None

    for i in range(1000):
        new_number = NewNumberUseCase(user_id)
        assert new_number.random_number is None

        _ = await new_number.execute()
        assert new_number.random_number is not None
        assert NewNumberUseCase.MIN <= new_number.random_number <= NewNumberUseCase.MAX

    get_number = GetNumberUseCase(user_id)
    assert get_number.random_number is None

    _ = await get_number.execute()
    assert get_number.random_number is not None
    assert NewNumberUseCase.MIN <= get_number.random_number <= NewNumberUseCase.MAX

    user = await users.get(user_id)
    assert user is not None
    assert user.random_number == get_number.random_number
