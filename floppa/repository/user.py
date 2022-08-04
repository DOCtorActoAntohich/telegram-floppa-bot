import pymotyc  # type: ignore

from floppa.models import User
from floppa.storage import Storage
from floppa.repository.base import MongoRepository


class UserRepository(MongoRepository[User, int]):
    @classmethod
    def create(cls):
        return cls(Storage.users)

    def __init__(self, collection: pymotyc.Collection[User]):
        super().__init__(collection)

    def identity_field(self, /):
        return User.user_id
