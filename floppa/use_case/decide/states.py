from enum import IntEnum, auto


class DecideUseCaseState(IntEnum):
    NotExecuted = auto()
    NoOptions = auto()
    Success = auto()


class DecideUseCaseMode(IntEnum):
    Unknown = auto()
    OneLine = auto()
    MultiLine = auto()
