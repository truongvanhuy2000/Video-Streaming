from WebServer.Config.config import CONFIG
import logging
import sys

_LOGGER = logging.getLogger("HuyLog")
logging.getLogger('werkzeug').disabled = True

def setUpLogging():
    global _LOGGER
    handler = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter('[PID %(process)d] %(message)s')
    formatter = logging.Formatter('{%(filename)s:%(lineno)d}[%(threadName)s] - %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(levelConfig())
    sys.stdout.flush()

def levelConfig():
    level = logging.NOTSET
    match CONFIG.logging_level:
        case "DEBUG":
            level = logging.DEBUG
        case "INFO":
            level = logging.INFO
        case "ERROR":
            level = logging.ERROR
        case "WARNING":
            level = logging.WARNING
        case "WARN":
            level = logging.WARN
    return level
    