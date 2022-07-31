import random

from floppa.models import User
from floppa.repository import UserRepository
from floppa.use_case.new_number.responses import NewNumberResponse


class NewNumberUseCase:
    MIN = 0
    MAX = 1000

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.users = UserRepository.create()

    async def execute(self) -> str:
        user = await self.users.get(self.user_id)
        if user is None:
            user = await self.users.save(User(user_id=self.user_id))

        user.random_number = random.randint(self.MIN, self.MAX)
        await self.users.update(user)

        return NewNumberResponse.new_number(user.random_number)
