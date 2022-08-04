class ValidateBracketsUseCase:
    def __init__(self, text: str):
        self.text = text

    async def execute(self) -> str | None:
        left = self.text.count("(")
        right = self.text.count(")")
        if left == right:
            return None

        n_times = abs(left - right)
        missing_bracket = "(" if left < right else ")"

        return missing_bracket * n_times
