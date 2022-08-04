from enum import IntEnum, auto


class ExecuteCommandUseCaseState(IntEnum):
    NotExecuted = auto()

    CommandNotFound = auto()

    Success = auto()
