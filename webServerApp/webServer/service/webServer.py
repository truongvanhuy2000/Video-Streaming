from flask import Flask, Response, render_template, request, redirect, url_for
import os

from webServer.transportation import protocolProvider
from webServer.db.persistentData import persistentData
from webServer.common import logger

import threading

lock = threading.RLock()
lock.acquire()

# Set up environment variable
GRPC_SERVER1 = os.getenv('GRPC_SERVER1')
GRPC_SERVER2 = os.getenv('GRPC_SERVER2')
GRPC_SERVER3 = os.getenv('GRPC_SERVER3')
GRPC_SERVER4 = os.getenv('GRPC_SERVER4')
TRANSPORT_METHOD = os.getenv('TRANSPORT_METHOD')

# GRPC_SERVER1 = '192.168.42.63:9876'
# GRPC_SERVER2 = '192.168.42.63:9876'
# GRPC_SERVER3 = '192.168.42.63:9876'
# GRPC_SERVER4 = '192.168.42.63:9876'
# TRANSPORT_METHOD = 'GRPC'

if (GRPC_SERVER1 is None) and (GRPC_SERVER2 is None) and (GRPC_SERVER3 is None) and (GRPC_SERVER4 is None) and (TRANSPORT_METHOD is None): 
    print("Missing environment variable")
    exit()

db = persistentData('webServer/db/persistentData.json')
app = Flask(__name__)

video_feeds = [
    'video_feed_one',
    'video_feed_two',
    'video_feed_three',
    'video_feed_four'
]
status = None

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        aiModel = request.form['Model']
        view = int(request.form['View'])
        data = {
            'model': aiModel,
            'view': view,
        }
        db.writeData(data)
    else:
        if db.isEmpty():
            aiModel = 'generic'
            view = 2
        else:
            aiModel = db.readData('model')
            view = db.readData('view')
    return render_template('index.html', model=aiModel, views=int(view), video_feeds=video_feeds, status = status)

@app.route('/status', methods=['POST', ])
def status():
    global status
    action = request.form['action']
    # Handle the action value accordingly
    if action == "start":
        status = "start"
    else:
        status = "stop"
    return redirect(url_for('index'))

@app.route('/<variable>/video_feed_one')
def video_feed_one(variable):
    return handleVideoFeed(model=variable, video="video1", addr=GRPC_SERVER1)

@app.route('/<variable>/video_feed_two')
def video_feed_two(variable):
    return handleVideoFeed(model=variable, video="video2", addr=GRPC_SERVER2)

@app.route('/<variable>/video_feed_three')
def video_feed_three(variable):
    return handleVideoFeed(model=variable, video="video3", addr=GRPC_SERVER3)

@app.route('/<variable>/video_feed_four')
def video_feed_four(variable):
    return handleVideoFeed(model=variable, video="video4" ,addr=GRPC_SERVER4)

def handleVideoFeed(model, video, addr):
    if status != "start":
        return None
    
    transportMethod = protocolProvider.getTransportMethod(method=TRANSPORT_METHOD)
    
    return Response(transportMethod.request(video=video, 
                                            model=model,
                                            addr=addr),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def runWebServer():
    app.run(host="0.0.0.0", debug=False)