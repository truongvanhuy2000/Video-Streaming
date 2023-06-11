from flask import Flask, Response, render_template, request, redirect, url_for
import os

from webServer.transportation import protocolProvider
from webServer.db.persistentData import persistentData
import threading
from webServer.common import logger 
import socket

# Set up environment variable
GRPC_SERVER1 = os.getenv('GRPC_SERVER1')
GRPC_SERVER2 = os.getenv('GRPC_SERVER2')
GRPC_SERVER3 = os.getenv('GRPC_SERVER3')
GRPC_SERVER4 = os.getenv('GRPC_SERVER4')
TRANSPORT_METHOD = os.getenv('TRANSPORT_METHOD')

if (GRPC_SERVER1 is None) and (GRPC_SERVER2 is None) and (GRPC_SERVER3 is None) and (GRPC_SERVER4 is None) and (TRANSPORT_METHOD is None): 
    print("Missing environment variable")
    exit()


app = Flask(__name__)
status = None

_PORT_ = 7654

@app.route('/', methods=['POST', 'GET'])
def index():
    video_feeds = [
        'video_feed_one',
        'video_feed_two',
        'video_feed_three',
        'video_feed_four'
    ]
    db = persistentData('webServer/db/persistentData.json')

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
    status = "start" if action == "start" else "stop"
    return redirect(url_for('index'))

@app.route('/<variable>/video_feed_one')
def video_feed_one(variable):
    return handleVideoFeed(variable=variable, video="video1", addr=GRPC_SERVER1)

@app.route('/<variable>/video_feed_two')
def video_feed_two(variable):
    return handleVideoFeed(variable=variable, video="video2", addr=GRPC_SERVER2)

@app.route('/<variable>/video_feed_three')
def video_feed_three(variable):
    return handleVideoFeed(variable=variable, video="video3", addr=GRPC_SERVER3)

@app.route('/<variable>/video_feed_four')
def video_feed_four(variable):
    return handleVideoFeed(variable=variable, video="video4", addr=GRPC_SERVER4)

def handleVideoFeed(variable, video, addr):
    if status != "start":
        return None
    # Print the thread identifier
    logger._LOGGER.info("Current Thread: " + threading.current_thread().name)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', _PORT_))
    request = "CONNECT"
    s.sendall(request.encode())
    response = s.recv(2048).decode()
    
    logger._LOGGER.info(f"Response from server is {response}")

    transportMethod = protocolProvider.getTransportMethod(TRANSPORT_METHOD)
    return Response(transportMethod.request(video=video, 
                                            model=variable, 
                                            addr=addr, sock=s),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def runWebServer():
    app.run(host="0.0.0.0", debug=False, )