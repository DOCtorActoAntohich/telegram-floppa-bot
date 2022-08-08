import pytest

from floppa.models import Command
from floppa.use_case.cat import GetCatThatDoesNotExist


@pytest.mark.asyncio
async def test_cat():
    command, args = Command.parse("/cat")
    assert command is not None and command.formatted == "/cat"
    # Get image.
    await GetCatThatDoesNotExist().execute()
