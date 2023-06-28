from VideoServer import app
from VideoServer.common import logger

if __name__ == '__main__':
    logger.setUpLogging()
    app.run()