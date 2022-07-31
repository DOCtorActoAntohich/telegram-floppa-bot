import random

from floppa.use_case.decide.responses import DecideCommandResponse


class DecideUseCase:
    def __init__(self, text: str | None):
        if text is None:
            text = ""

        per_line_options = text.split("\n")
        if len(per_line_options) != 1:
            self.options = [o for o in per_line_options if len(o) == 0 or o.isspace()]
            return

        self.options = text.split()

    async def execute(self) -> str:
        if not self.options:
            return DecideCommandResponse.no_options()

        one = random.choice(self.options)
        return DecideCommandResponse.chosen(one)
