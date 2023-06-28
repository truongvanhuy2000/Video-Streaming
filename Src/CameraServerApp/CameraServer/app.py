from CameraServer.VideoPublisher.publisher import videoPublisher
from CameraServer.VideoReader.cv2Reader import camera_server
from CameraServer.common.logger import _LOGGER
from CameraServer.common import helper
from CameraServer.Config.config import CONFIG

import json
import os

RESOURCE = CONFIG.resource
RABBITMQ_HOST = CONFIG.rabbitmq_host
CAMERA_NAME = CONFIG.camera_name

if any(item is None for item in [RESOURCE, RABBITMQ_HOST, CAMERA_NAME]):
    _LOGGER.error("Missing config")
    exit()

def createMetaData(camera : camera_server, exchange, topic) -> str:
    parameters = ['height', 'width', 'fps']
    cameraInfo = {}

    metadata = camera.getCaptureInformation(parameters)

    metadata['exchange'] = exchange
    metadata['topic'] = topic
    
    cameraInfo['camera'] = CAMERA_NAME
    cameraInfo['metadata'] = metadata
    return json.dumps(cameraInfo)

def run():
    camera = camera_server(f"CameraServer/resources/{RESOURCE}")
    publisher = videoPublisher(RABBITMQ_HOST)
        
    publisher.createQueue(queue='metadata', durable=True)
    metadata = createMetaData(camera=camera, exchange='video_exchange', topic=CAMERA_NAME)
    _LOGGER.info(metadata)
    publisher.publish(exchange='', routing_key='metadata', data=metadata, persistent=True)

    while True:
        frame = camera.readVideo()
        serializeData = helper.serializeTheImage(frame)
        if publisher.createExchange(exchange='video_exchange') is not None:
            publisher.publish(exchange='video_exchange', routing_key=CAMERA_NAME, data=serializeData)
    