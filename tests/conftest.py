import asyncio
import random

import pytest


# Fixed the "Event loop is closed" problem
# When running second file (any) with async tests.
@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def random_ids(request) -> list[int]:
    amount = request.param
    left = 0
    right = 2**32
    assert 1 <= amount < right, "Test with mistake :)"
    return random.sample(range(left, right), amount)
