from re import I
from floppa.models import User
from floppa.repository import UserRepository
from floppa.use_case.toggle_brackets.responses import ToggleBracketsResponse


class ToggleBracketsUseCase:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.users = UserRepository.create()

    async def execute(self) -> str:
        user = await self.users.get(self.user_id)
        if user is None:
            user = await self.users.save(User(user_id=self.user_id))

        user.validate_brackets = not user.validate_brackets
        await self.users.update(user)

        if user.validate_brackets:
            return ToggleBracketsResponse.on_enabled()

        return ToggleBracketsResponse.on_disabled()
