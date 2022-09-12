from re import L
from floppa.models import User
from floppa.repository import UserRepository


class ValidateBracketsUseCase:
    def __init__(self, user_id: int, text: str):
        self.user_id = user_id
        self.users = UserRepository.create()
        self.text = text

    async def execute(self) -> str | None:
        user = await self.users.get(self.user_id)
        if user is None:
            user = await self.users.save(User(user_id=self.user_id))

        if not user.validate_brackets:
            return None

        left = self.text.count("(")
        right = self.text.count(")")
        if left == right:
            return None

        n_times = abs(left - right)
        missing_bracket = "(" if left < right else ")"

        return missing_bracket * n_times
