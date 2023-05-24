from videoServer.proto import image_pb2, image_pb2_grpc
from videoServer.service.cameraServer import camera_server
from videoServer.common import helper

import grpc
from concurrent import futures
import socket
import logging
import cv2
import sys
import multiprocessing

_LOGGER = logging.getLogger(__name__)
_PROCESS_COUNT = multiprocessing.cpu_count()
_PORT_ = 9876

class imageTranfer(image_pb2_grpc.image_tranferServicer):
    def __init__(self) -> None:
        super().__init__()

    def send_me_image(self, request, context):
        _LOGGER.info("User request video: " + request.video + " with model: " + request.model)
        # print("User request video: " + request.video + " with model: " + request.model)
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
    
# This will intercept the connection to prevent multiple client connect to the same server
# class SingleConnectionInterceptor(grpc.ServerInterceptor):
#     def __init__(self, service) -> None:
#         self.maxlimit = 1
#         self.service = service

#     def intercept_service(self, continuation, handler_call_details):
#         _LOGGER.info("interceptor running")

#         if self.service.getCurrentActiveConnection() <= 1:
#             return continuation(handler_call_details)
# interceptors=(SingleConnectionInterceptor(myService),)

def runServer(address):
    _LOGGER.info("start a new server")
    # interceptors=(SingleConnectionInterceptor(),)
    myService = imageTranfer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), maximum_concurrent_rpcs=1)
    image_pb2_grpc.add_image_tranferServicer_to_server(myService, server)

    server.add_insecure_port(address)
    server.start()
    server.wait_for_termination()

def startSocket():
    """Find and reserve a port for all subprocesses to use."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT.")
    sock.bind(('0.0.0.0', _PORT_))
    print(f"The server is listening on address: {sock.getsockname()[0]}:{sock.getsockname()[1]}")
    return sock.getsockname()[1]

def setUpLogging():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)
    sys.stdout.flush()

def serve():
    setUpLogging()
    port = startSocket()
    bind_address = 'localhost:{}'.format(port)
    workers = []
    for _ in range(_PROCESS_COUNT):
        worker = multiprocessing.Process(target=runServer,
                                            args=(bind_address,))
        worker.start()
        workers.append(worker)
    for worker in workers:
        worker.join()