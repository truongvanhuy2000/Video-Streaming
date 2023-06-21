from cameraServer.VideoPublisher.publisher import videoPublisher
from cameraServer.VideoReader.cv2Reader import camera_server
from cameraServer.common import logger
from cameraServer.common import helper

import json
import os

VIDEO_DIRECTORY = os.getenv('RESOURCE_DIR')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
CAMERA_NAME = os.getenv('CAMERA_NAME')

if any in [VIDEO_DIRECTORY, RABBITMQ_HOST, CAMERA_NAME] is None:
    logger._LOGGER.error("Missing env")
    exit()

def createMetaData(camera : camera_server, exchange, topic) -> str:
    parameters = ['height', 'width', 'fps']
    metadata = camera.getCaptureInformation(parameters)

    metadata['exchange'] = exchange
    metadata['topic'] = topic

    return json.dumps(metadata)

def run():
    cam = camera_server(VIDEO_DIRECTORY)
    publisher = videoPublisher(RABBITMQ_HOST)

    metadata = createMetaData(camera=cam, exchange='video_exchange', topic=CAMERA_NAME)
    logger._LOGGER.info(f'Meta data is {metadata}')
    publisher.publishToQueue(data=metadata)

    while True:
        frame = cam.readVideo()
        serializeData = helper.serializeTheImage(frame)
        publisher.publishToExchange(topic=CAMERA_NAME, data=serializeData)
    