from WebServer import app
from WebServer.common import logger
if __name__ == '__main__':
    logger.setUpLogging()
    app.run()