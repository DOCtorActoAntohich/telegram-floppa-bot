import random

import pytest
from pymotyc.errors import NotFound  # type: ignore

from floppa.models import Chat, ChatType, Command
from floppa.repository import ChatRepository
from floppa.storage import connect_to_database


def random_id():
    return random.randint(0, 2**32)


@pytest.mark.asyncio
async def test_mongo_chat_repository():
    await connect_to_database()

    chats = ChatRepository.create()

    id_0 = random_id()
    id_1 = random_id()
    id_2 = random_id()
    id_3 = random_id()
    id_bad = random_id()

    empty_list = await chats.get_all()
    assert len(empty_list) == 0, "The collection must be empty"

    zero_id_exists = await chats.exists(chat_id=id_0)
    assert not zero_id_exists, "The collection must be empty"

    deleted_zero = await chats.delete(chat_id=id_0)
    assert not deleted_zero, "The collection must be empty"

    zero_none = await chats.get(chat_id=id_0)
    assert zero_none is None, "The collection must be empty"

    chat_negative = await chats.update(Chat(chat_id=id_bad))
    assert chat_negative is None, "There should be no such object."

    await chats.save(Chat(chat_id=id_0))
    await chats.save(Chat(chat_id=id_1))
    await chats.save(Chat(chat_id=id_2))

    three_chats = await chats.get_all()
    assert len(three_chats) == 3, "3 chats must exist in any order"

    chat_3 = await chats.save(Chat(chat_id=id_3))
    assert chat_3 is not None, "Copy of saved object should be returned"

    chat_0 = await chats.get(chat_id=id_0)
    chat_1 = await chats.get(chat_id=id_1)
    chat_2 = await chats.get(chat_id=id_2)
    chat_3 = await chats.get(chat_id=id_3)
    assert chat_0.chat_id == id_0
    assert chat_1.chat_id == id_1
    assert chat_2.chat_id == id_2
    assert chat_3.chat_id == id_3

    chat_0.commands.set(
        Command(name="zero", chat_type=ChatType.Private, is_hidden=True), "0"
    )
    chat_0.commands.set(Command(name="ping"), "@everyone")

    chat_0_copy = await chats.update(chat_0)
    assert chat_0_copy is not None, "Copy of saved object should be returned"

    response_zero = chat_0_copy.commands.get_response(Command(name="zero"))
    response_ping = chat_0_copy.commands.get_response(Command(name="ping"))
    assert response_zero == "0"
    assert response_ping == "@everyone"

    chat_0_copy.commands.delete(Command(name="zero"))
    await chats.update(chat_0_copy)

    await chats.delete(chat_id=id_1)
    await chats.delete(chat_id=id_2)
    await chats.delete(chat_id=id_3)
    one_chat = await chats.get_all()
    assert len(one_chat) == 1, "There should be one chat left now"

    chat_0_latest = await chats.get(chat_id=id_0)
    index = chat_0_latest.commands.index_of(Command(name="zero"))
    assert index is None, "The command should be deleted by now"

    zero_exists = await chats.exists(chat_id=id_0)
    assert zero_exists, "Chat with this ID must be in the collection"

    deleted_zero = await chats.delete(chat_id=id_0)
    assert deleted_zero, "Deletion should be successful"

    zero_exists = await chats.exists(chat_id=id_0)
    assert not zero_exists, "Chat with this ID must be already deleted"
