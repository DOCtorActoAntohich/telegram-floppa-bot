from enum import IntEnum, auto


class SetCommandUseCaseState(IntEnum):
    NotExecuted = auto()

    NoCommand = auto()
    NoResponse = auto()
    MalformedCommand = auto()
    BuiltinOverride = auto()

    Success = auto()
