import enum

class UserCommandType(enum.Enum):
    NONE = 0,
    CLEAR = 1, 
    LOG = 2,
    READ = 3,
    END = 4