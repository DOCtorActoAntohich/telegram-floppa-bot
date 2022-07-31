import random


class YesNoUseCase:
    options = ["Yes", "No"]

    async def execute(self):
        return random.choice(self.options)
