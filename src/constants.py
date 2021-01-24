from enum import IntEnum


class Level(IntEnum):
    DEBUG = 0
    NOTICE = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class Output(IntEnum):
    SCREEN = 0
    FILE = 1
    TEE = 2

DEFAULT_LOG_FILE = './default.log'
