from flask import Flask, Response, render_template, request, redirect, url_for
from WebServer.Transportation import transportProvider
from WebServer.common.logger import _LOGGER 
from WebServer.Database import databaseProvider
from WebServer.Config.config import CONFIG

import json

# Configuration for connection to database
DATABASE_TYPE = CONFIG.database_type
DATABASE_HOST = CONFIG.database_host
DATABASE_PORT = CONFIG.database_port

# Configuration for connection to load balancer
LOADBALANCER_TRANSPORT_METHOD = CONFIG.loadbalancer_transport_method
LOADBALANCER_HOST = CONFIG.loadbalancer_host
LOADBALANCER_PORT = CONFIG.loadbalancer_port

app = Flask(__name__)
database = databaseProvider.getDatabase(type=DATABASE_TYPE, 
                                        host=DATABASE_HOST, 
                                        port=DATABASE_PORT, 
                                        db=1)
status = None

@app.route('/', methods=['POST', 'GET'])
def index():
    video_feeds = sorted(requestCameraList(), key=lambda x: int(x[-1]))
    ai_models = requestAiModelList()
    
    if request.method == 'POST':
        aiModel = request.form['Model']
        camera = request.form['Camera']
        data = {
            'model': aiModel,
            'camera': camera
        }
        database.setData('viewConfig', json.dumps(data))

    else:
        config = database.getData('viewConfig')

        if config is None:
            aiModel = 'None'
            camera = 'camera1'
        else:
            config = json.loads(config)
            aiModel = config.get('model', 'None')
            camera = config.get('camera', 'camera1')

    return render_template('index.html', model=aiModel, 
                           camera=camera, video_feeds=video_feeds, 
                           ai_models=ai_models, status=status)

def requestCameraList() -> list:
    transportMethod = transportProvider.getTransportMethod(method=LOADBALANCER_TRANSPORT_METHOD, 
                                                                host=LOADBALANCER_HOST,
                                                                port=LOADBALANCER_PORT)
    
    response = transportMethod.request("/camera_list_request", data="")
    transportMethod.close()
    try:
        cameraList = json.loads(response)
    except Exception as e:
        _LOGGER.error(f"{e}")
        return []
    return cameraList.get('camera')

def requestAiModelList() -> list:
    transportMethod = transportProvider.getTransportMethod(method=LOADBALANCER_TRANSPORT_METHOD, 
                                                                host=LOADBALANCER_HOST,
                                                                port=LOADBALANCER_PORT)
    
    response = transportMethod.request("/ai_model_list", data="")
    transportMethod.close()
    try:
        aiModelList = json.loads(response)
    except Exception as e:
        _LOGGER.error(f"{e}")
        return []
    return aiModelList.get('models')

@app.route('/status', methods=['POST', ])
def status():
    global status
    action = request.form['action']
    status = "start" if action == "start" else "stop"
    return redirect(url_for('index'))

@app.route('/camera_feed/<camera>/<model>')
def camera_feed(model, camera):
    _LOGGER.info(f"Request {camera} using model {model}")
    videoRequest = {
        'model': model,
        'camera' : camera
        }
    videoRequest = json.dumps(videoRequest)
    return Response(connectionToVideoService(request=videoRequest),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def connectionToVideoService(request):
    try:
        transportMethod = transportProvider.getTransportMethod(method=LOADBALANCER_TRANSPORT_METHOD, 
                                                                host=LOADBALANCER_HOST,
                                                                port=LOADBALANCER_PORT)
        while True: 
            response = transportMethod.request(route='/video_request', data=request)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + response + b'\r\n')

    except GeneratorExit as e:
        _LOGGER.warning(f"Close the connection")
        transportMethod.close()
        return Response(status=500)

    
    