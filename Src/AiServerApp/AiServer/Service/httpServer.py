from AiServer.common.logger import _LOGGER
from AiServer.common import helper
from AiServer.AiProcessor.faceDetection import faceDetection
from AiServer.Config.config import CONFIG

from flask import Flask
from flask import request as httpRequest, Response
from queue import Queue

import threading
import json

# Configuration for server hosting
HTTPSERVER_HOST = CONFIG.httpserver_host
HTTPSERVER_PORT = CONFIG.httpserver_port

app = Flask(__name__)
rLock = threading.RLock()

requestQueue = Queue()
responseQueue = Queue()

@app.route('/', methods=['POST', 'GET'])
def handleRequest():
    requestBody = httpRequest.get_json()
    if requestBody is None:
        return Response(response='Missing argument', status=500)
    
    rLock.acquire()
    requestQueue.put(requestBody)
    response = responseQueue.get()
    rLock.release()
    
    return Response(content_type='application/json', response=response, status=200)

def flaskHandler():
    _LOGGER.info("Http Server is running")

    app.run(host=HTTPSERVER_HOST,
            port=HTTPSERVER_PORT, 
            debug=False)

def faceDetectionHandler():
    _LOGGER.info("Face Detection is running")
    while True:
        request = requestQueue.get()
        
        frame = request.get('frame', None)
        model = request.get('model', None)

        if any(item is None for item in [frame, model]):
            _LOGGER.error("Missings frame/model data")
            continue
        faces = faceDetection(model).detect(helper.decodeToByte(frame))

        responseQueue.put(item=faces)

def serve():
    faceDetectThread = threading.Thread(target=faceDetectionHandler)
    httpServerThread = threading.Thread(target=flaskHandler)

    faceDetectThread.start()
    httpServerThread.start()

    faceDetectThread.join()
    httpServerThread.join()
