import logging
import sys

_LOGGER = logging.getLogger("HuyLog")
logging.getLogger('werkzeug').disabled = True

def setUpLogging():
    handler = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter('[PID %(process)d] %(message)s')
    formatter = logging.Formatter('{%(filename)s:%(lineno)d} - %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.DEBUG)
    sys.stdout.flush()

setUpLogging()