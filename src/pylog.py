from datetime import datetime
from constants import Level, Output, DEFAULT_LOG_FILE
from exceptions import LevelNotAllowedException, OutputNotAllowedException


# Log levels
DEBUG = Level.DEBUG
NOTICE = Level.NOTICE
INFO = Level.INFO
WARNING = Level.WARNING
ERROR = Level.ERROR
CRITICAL = Level.CRITICAL
ALLOWED_LEVELS = [DEBUG, NOTICE, INFO, WARNING, ERROR, CRITICAL]
#Output options
SCREEN = Output.SCREEN
FILE = Output.FILE
TEE = Output.TEE
ALLOWED_OUTPUTS = [SCREEN, FILE, TEE]


class Logger:
    def __init__(self, level=INFO, output=SCREEN, path=DEFAULT_LOG_FILE):
        self.level = level
        self.path = path
        self.launcher = 'FILE:%s' % str(__file__.split('/')[::-1][0])
        self.action = self.setOutput(output)

    def checkInAllowed(self, arg, allowed, exception):
        if getattr(self, str(arg.__name__)) in allowed:
            setattr(self, str(arg.__name__), arg)
        else:
            raise exception

    def setLevel(self, level: Level):
        if level in ALLOWED_LEVELS:
            self.level = level
        else:
            raise LevelNotFoundException

    def setOutput(self, output: Output):
        ACTIONS= {
            SCREEN: self.screen,
            FILE: self.write,
            TEE: self.tee,
        }
        if output in ALLOWED_OUTPUTS:
            self.action = ACTIONS.get(output)
        else:
            raise OutputNotFoundException

    # Actions
    def formatMsg(self, msgText, level):
        time = datetime.now()
        _level = repr(level)
        level = f"[{_level}]"
        date = f"{time.day}-{time.month}-{time.year} {time.hour}:{time.minute}:{time.second}.{time.microsecond}"
        msg = f"{level}\t{date}\t{self.launcher}\t{msgText}"
        return msg

    def screen(self, msgText, level):
        msg = self.formatMsg(msgText, level)
        print(msg)

    def write(self, msgText, level):
        msg = self.formatMsg(msgText, level)
        with open(self.path, 'a+') as myfile:
            myfile.write('%s\n' % msg)

    def tee(self, msg, level):
        self.screen(msg, level)
        self.write(msg, level)
    
    # Stream handling
    def log(self, msg, level: Level):
        if self.level <= level:
            self.action(msg, level)

    def debug(self, msg):
        self.log(msg, DEBUG)
    
    def notice(self, msg):
        self.log(msg, NOTICE)

    def info(self, msg):
        self.log(msg, INFO)

    def warning(self, msg):
        self.log(msg, WARNING)

    def error(self, msg):
        self.log(msg, ERROR)

    def critical(self, msg):
        self.log(msg, CRITICAL)


class Loggable:
    def __init__(self):
        self.logger = Logger()
        self.logger.launcher = 'CLASS:%s' % str(self.__class__.__name__)

    def debug(self, msg):
        self.logger.debug(msg)

    def notice(self, msg):
        self.logger.notice(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
