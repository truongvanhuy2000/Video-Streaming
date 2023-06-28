from VideoServer.common import helper
from VideoServer.common.logger import _LOGGER
from VideoServer.MessageConsumer import consumerProvider
from VideoServer.Database import databaseProvider
from VideoServer.Transportation import transportProvider
from VideoServer.VideoProcessor.videoProcessor import videoProcessor
from VideoServer.Config.config import CONFIG

from flask import Flask, Response, request

import json
import threading

# Configuration for connection to database
DATABASE_TYPE = CONFIG.database_type
DATABASE_HOST = CONFIG.database_host
DATABASE_PORT = CONFIG.database_port

# Configuration for connection to load balancer
LOADBALANCER_TRANSPORT_METHOD = CONFIG.loadbalancer_transport_method
LOADBALANCER_HOST = CONFIG.loadbalancer_host
LOADBALANCER_PORT = CONFIG.loadbalancer_port

# Configuration for server hosting
HTTPSERVER_HOST = CONFIG.httpserver_host
HTTPSERVER_PORT = CONFIG.httpserver_port

RABBITMQ_HOST = CONFIG.rabbitmq_host

app = Flask(__name__)
rLock = threading.RLock()
database = databaseProvider.getDatabase(type=DATABASE_TYPE,
                                        host=DATABASE_HOST, 
                                        port=DATABASE_PORT, 
                                        db=0)

def getVideo(host, metadata):
    metadata = json.loads(metadata)
    topic = metadata.get('topic')
    exchange = metadata.get('exchange')
    
    if any(item is None for item in [topic, exchange]):
        _LOGGER.error("Missing topic and exchange information")
        return 500
    
    messageConsumer = consumerProvider.startConsumer(type="RABBIT_MQ", host=host)
    
    _, queue = messageConsumer.createTopic(exchange=exchange,
                                        exchange_type='direct',
                                        queue='', 
                                        routing_key=topic, 
                                        binding=True, 
                                        exclusive=True, 
                                        durable=True)
    while True:
        videoData = messageConsumer.consume(queue)
        if videoData is not None:
            break

    # There still problem in this code --------------------------------
    messageConsumer.closeConnection()
    # There still problem in this code --------------------------------

    return videoData

def requestFaceDetection(requestData, frame):
    client = transportProvider.getTransportMethod(method=LOADBALANCER_TRANSPORT_METHOD, 
                                                  host=LOADBALANCER_HOST,
                                                  port=LOADBALANCER_PORT)
    response = client.request(requestData)
    if response is None:
        return frame
    
    faces = response.get('faces')
    detectedFrame = videoProcessor().drawBoundingBox(helper.deserializeTheImage(frame), faces)
    # Look up database for face recognition-----------------------------------------
    #LookUpDatabaseForFaceRecognition()
    #-------------------------------------------------------------------------------
    return helper.serializeTheImage(detectedFrame)


@app.route('/', methods=['POST', 'GET'])
def handleRequest():
    data = request.get_json()
    if data is None:
        return Response(response='Missing request', status=500)
    
    camera = data.get('camera', None)
    model = data.get('model', None)
    if any(item is None for item in [camera, model]):
        return Response(response='Missing request', status=500)

    # Critical section-----------------------------------------------------------
    rLock.acquire()
    metadata = database.getData(camera)
    rLock.release()
    #Critical section------------------------------------------------------------

    videoData = getVideo(host=RABBITMQ_HOST, metadata=metadata)

    tempDict = {
        'model' : model,
        'frame' : helper.encodeToString(videoData)
    }
    frame = requestFaceDetection(json.dumps(tempDict), videoData)

    return Response(response=frame, status=200)

def serve():
    _LOGGER.info("Http Server is running")
    app.run(host=HTTPSERVER_HOST, port=HTTPSERVER_PORT, debug=False)