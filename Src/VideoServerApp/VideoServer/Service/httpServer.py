from flask import Flask, Response, request
from VideoServer.common import logger
from VideoServer.MessageConsumer import consumerProvider

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def handleRequest():
    data = request.get_json()
    if data is None:
        return "Missing request"
    camera = data.get('camera')

    # ------------------------------------------------------------
    # topic = lookupDB(camera)
    #-------------------------------------------------------------

    messageConsumer = consumerProvider.startConsumer(type="RABBIT_MQ", host='localhost')
    _, queue = messageConsumer.createTopic(exchange='video_exchange', 
                                                queue=topic, 
                                                routing_key='', 
                                                binding=True, 
                                                exclusive=True, 
                                                durable=True)


def serve():
    app.run(host="0.0.0.0", debug=False)