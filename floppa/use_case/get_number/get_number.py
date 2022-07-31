from floppa.models import User
from floppa.repository import UserRepository
from floppa.use_case.get_number.responses import GetNumberResponse


class GetNumberUseCase:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.users = UserRepository.create()

    async def execute(self) -> str:
        user = await self.users.get(self.user_id)
        if user is None:
            user = await self.users.save(User(user_id=self.user_id))

        if user.random_number is None:
            return GetNumberResponse.no_random_number()

        return GetNumberResponse.random_number_found(user.random_number)
