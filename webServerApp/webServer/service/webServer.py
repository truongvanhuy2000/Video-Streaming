from flask import Flask, Response, render_template, request, redirect, url_for
import os

from webServer.transportation import protocolProvider
from webServer.db.persistentData import persistentData
import threading
from webServer.common import logger 
import socket
import asyncio

# Set up environment variable
TRANSPORT_METHOD = os.getenv('TRANSPORT_METHOD')
LOAD_BALANCER_ADDR = 'loadbalancer'
LOAD_BALANCER_PORT = os.getenv('LOAD_BALANCER_PORT')
VIDEO_SERVER_PORT = int(os.getenv('VIDEO_SERVER_PORT'))

if any(var is None for var in [VIDEO_SERVER_PORT, TRANSPORT_METHOD, LOAD_BALANCER_PORT]):
    logger._LOGGER.error("Missing environment variable")
    exit()

app = Flask(__name__)
loop = asyncio.get_event_loop()

status = None

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
    return handleVideoFeed(variable=variable, video="video1")

@app.route('/<variable>/video_feed_two')
def video_feed_two(variable):
    return handleVideoFeed(variable=variable, video="video2")

@app.route('/<variable>/video_feed_three')
def video_feed_three(variable):
    return handleVideoFeed(variable=variable, video="video3")

@app.route('/<variable>/video_feed_four')
def video_feed_four(variable):
    return handleVideoFeed(variable=variable, video="video4")

def handleConnectionToService(video, model, transportMethod, sock):

    try:
        yield from transportMethod.request(video, model)
    except:
        logger._LOGGER.info(f"Send close request to server")
        sock.sendall("CLOSE".encode())
        sock.close()

def handleVideoFeed(variable, video):
    if status != "start":
        return None
    # Print the thread identifier
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger._LOGGER.info(f"Try to connect to loadbalancer:{LOAD_BALANCER_PORT}")

    sock.connect(('loadbalancer', 7654))
    sock.sendall("CONNECT".encode())
    response = sock.recv(2048).decode()

    logger._LOGGER.info(f"Response from server is {response}")

    transportMethod = protocolProvider.getTransportMethod(method=TRANSPORT_METHOD, address=f"{response}:{VIDEO_SERVER_PORT}")
    loop.run_until_complete(transportMethod.waitForServer()) 

    return Response(handleConnectionToService(video=video, 
                                            model=variable,
                                            transportMethod=transportMethod,
                                            sock=sock),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def runWebServer():
    app.run(host="0.0.0.0", debug=False)
    