from CameraServer import app
from CameraServer.common import logger

if __name__ == '__main__':
    logger.setUpLogging()
    app.run()