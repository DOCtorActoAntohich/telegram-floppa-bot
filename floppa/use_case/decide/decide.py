import random


class DecideUseCase:
    def __init__(self, text: str):
        ...

    async def execute(self) -> str:
        ...
