from io import BytesIO

from aiogram.types import Message, InputFile  # type: ignore

from floppa.models import ProtectedCommand
from floppa.telegram import floppa_bot
from floppa.use_case.cat import GetCatThatDoesNotExist


@floppa_bot.dispatcher.message_handler(ProtectedCommand.cat.filter)
async def cat(message: Message) -> None:
    with BytesIO(await GetCatThatDoesNotExist.execute()) as file:
        await message.reply_photo(InputFile(file))
