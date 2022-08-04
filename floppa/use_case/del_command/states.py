from enum import IntEnum, auto


class DeleteCommandUseCaseState(IntEnum):
    NotExecuted = auto()

    NoCommandProvided = auto()
    MalformedCommand = auto()
    BuiltinDelete = auto()
    CommandNotFound = auto()

    Success = auto()
