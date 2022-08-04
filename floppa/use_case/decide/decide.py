import random

from floppa.use_case.decide.states import DecideUseCaseState, DecideUseCaseMode
from floppa.use_case.decide.responses import DecideCommandResponse


class DecideUseCase:
    def __init__(self, text: str | None):
        self.state = DecideUseCaseState.NotExecuted
        self.mode = DecideUseCaseMode.Unknown
        self.selected_option = ""

        if text is None:
            text = ""

        lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 0]

        if len(lines) == 0:
            self.options = []
            return

        if len(lines) == 1:
            self.mode = DecideUseCaseMode.OneLine
            self.options = text.split()
            return

        self.options = lines
        self.mode = DecideUseCaseMode.MultiLine

    async def execute(self) -> str:
        if not self.options:
            self.state = DecideUseCaseState.NoOptions
            return DecideCommandResponse.no_options()

        one = random.choice(self.options)
        self.state = DecideUseCaseState.Success
        self.selected_option = one
        return DecideCommandResponse.chosen(one)
