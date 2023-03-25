import enum
from rx.subject import Subject # type: ignore[attr-defined]

class CommandType(enum.Enum):
    NONE = 0,
    CLEAR = 1, 
    LOG = 2,
    READ = 3,
    END = 4

class CommandTypeSubject(Subject):
    """
    内部の型をCommandTypeに限定したSubject。
    """
    def on_next(self, value: CommandType) -> None:
        super().on_next(value)