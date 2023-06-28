from AiServer import app
from AiServer.common import logger
if __name__ == '__main__':
    logger.setUpLogging()
    app.run()