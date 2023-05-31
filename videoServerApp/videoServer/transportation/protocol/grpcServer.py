from videoServer.proto import image_pb2, image_pb2_grpc
from videoServer.service.cameraServer import camera_server
from videoServer.common import helper
from videoServer.transportation.protocol.protocolServer import protocolServer

import grpc
from concurrent import futures
import logging
import sys

_LOGGER = logging.getLogger(__name__)

def setUpLogging():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)
    sys.stdout.flush()

class imageTranfer(image_pb2_grpc.image_tranferServicer):
    def __init__(self) -> None:
        super().__init__()

    def send_me_image(self, request, context):
        _LOGGER.info("User request video: " + request.video + " with model: " + request.model)
        self.camera = camera_server(model=request.model, video=request.video)

        while True:
            frame = self.camera.humanDetect()
            byteStream = helper.serializeTheImage(frame)
            img = image_pb2.image(data=byteStream)
            yield image_pb2.image_response(image_sent=img)
        # release the video capture object
    
    def ack(self, request, context):
        if (request.req == "done video"):
            self.camera.close()
            # cv2.destroyWindow("server")
            print("close video")
        return image_pb2.ack_response(rep="ok")
    
    def getCurrentActiveConnection(self):
        return self.activeConnection
    

class grpcServer(protocolServer):
    def serve(self, address):
        setUpLogging()
        _LOGGER.info("start a new server")
        # interceptors=(SingleConnectionInterceptor(),)
        myService = imageTranfer()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), maximum_concurrent_rpcs=1)
        image_pb2_grpc.add_image_tranferServicer_to_server(myService, server)

        server.add_insecure_port(address)
        server.start()
        server.wait_for_termination()


