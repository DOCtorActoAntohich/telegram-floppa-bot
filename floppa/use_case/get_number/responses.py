from floppa.models import ProtectedCommand


class GetNumberResponse:
    @classmethod
    def no_random_number(cls) -> str:
        return (
            f"You haven't set your number yet."
            f"Try {ProtectedCommand.new_number.formatted} first"
        )

    @classmethod
    def random_number_found(cls, number: int) -> str:
        return f"Your last random number was {number}"
