from typing import Callable, Coroutine
from aiogram.types import Message  # type: ignore

from floppa.models import ChatType
from floppa.settings import Settings
from floppa.telegram import floppa_bot
from floppa.telegram.utils import message_chat_type


AsyncMessageHandler = Callable[[Message], Coroutine[None, None, None]]


def _is_creator(user_id: int) -> bool:
    return user_id in Settings.bot.creator_ids


def _only_for_creators(old_handler: AsyncMessageHandler) -> AsyncMessageHandler:
    async def new_handler(message: Message) -> None:
        if not _is_creator(message.from_user.id):
            await message.reply("You. Just. Can't.")
            return
        await old_handler(message)

    return new_handler


def _only_for_chat_admins(old_handler: AsyncMessageHandler) -> AsyncMessageHandler:
    async def new_handler(message: Message) -> None:
        member = await floppa_bot.aiogram_bot.get_chat_member(
            chat_id=message.chat.id, user_id=message.from_user.id
        )
        if member.is_chat_admin() or _is_creator(message.from_user.id):
            await old_handler(message)

    return _only_group_chats(new_handler)


def _only_group_chats(old_handler: AsyncMessageHandler) -> AsyncMessageHandler:
    async def new_handler(message: Message) -> None:
        if message_chat_type(message) != ChatType.Group:
            await message.reply("That's a feature for group chats tbh")
            return
        await old_handler(message)

    return new_handler


def _only_private_chats(old_handler: AsyncMessageHandler) -> AsyncMessageHandler:
    async def new_handler(message: Message) -> None:
        if message_chat_type(message) != ChatType.Private:
            await message.reply("That's a feature for private messages tbh")
            return
        await old_handler(message)

    return new_handler


class CommandRestriction:
    only_for_creators = _only_for_creators
    only_for_chat_admins = _only_for_chat_admins

    only_group_chats = _only_group_chats
    only_private_chats = _only_private_chats
