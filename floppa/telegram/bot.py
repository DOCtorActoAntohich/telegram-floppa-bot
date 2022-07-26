from typing import Callable, Coroutine
import datetime

import aiogram

from floppa.settings import Settings


OnStartupReturnedCoroutineType = Coroutine[None, None, None]
OnStartupCallableType = Callable[[aiogram.Dispatcher, ...], OnStartupReturnedCoroutineType]


class _Bot:
    def __init__(self) -> None:
        self.__startup_time = datetime.datetime.now()
        self.__aiogram_bot: aiogram.Bot = aiogram.Bot(token=Settings.bot.token)
        self.__dispatcher: aiogram.Dispatcher = aiogram.Dispatcher(self.__aiogram_bot)

    @property
    def aiogram_bot(self) -> aiogram.Bot:
        return self.__aiogram_bot

    @property
    def alias(self) -> str:
        return Settings.bot.alias

    @property
    def dispatcher(self) -> aiogram.Dispatcher:
        return self.__dispatcher

    @property
    def startup_time(self) -> datetime.datetime:
        return self.__startup_time

    def run(self, *, on_startup: OnStartupCallableType):
        aiogram.executor.start_polling(self.__dispatcher, on_startup=on_startup, skip_updates=True)


floppa_bot = _Bot()
