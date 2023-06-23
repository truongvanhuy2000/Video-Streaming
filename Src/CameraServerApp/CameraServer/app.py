from CameraServer.VideoPublisher.publisher import videoPublisher
from CameraServer.VideoReader.cv2Reader import camera_server
from CameraServer.common import logger
from CameraServer.common import helper

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
    camera = camera_server(VIDEO_DIRECTORY)
    publisher = videoPublisher(RABBITMQ_HOST)

    publisher.createExchange(exchange='video_exchange')
    publisher.createQueue(queue='metadata', durable=True)

    metadata = createMetaData(camera=camera, exchange='video_exchange', topic=CAMERA_NAME)
    publisher.publish(exchange='video_exchange', routing_key='metadata', data=metadata, persistent=True)

    while True:
        frame = camera.readVideo()
        serializeData = helper.serializeTheImage(frame)
        publisher.publish(exchange='video_exchange', routing_key=CAMERA_NAME, data=serializeData)
    