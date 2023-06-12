from videoServer.proto import image_pb2, image_pb2_grpc
from videoServer.service.cameraServer import camera_server
from videoServer.common import helper
from videoServer.transportation.protocol.protocolServer import protocolServer
from videoServer.common import logger 
from concurrent import futures

import grpc

class imageTranfer(image_pb2_grpc.image_tranferServicer):
    def __init__(self) -> None:
        super().__init__()
        
    def are_you_ready(self, request, context):
        client_ip = context.peer().split(':')[1]
        client_port = context.peer().split(':')[2]
        if request.req is "READY":
            logger._LOGGER.info(f"{client_ip}:{client_port} want to know if i'm ready")
            return image_pb2.ready_response(rep="READY")

    def send_me_image(self, request, context):
        client_ip = context.peer().split(':')[1]
        client_port = context.peer().split(':')[2]
        logger._LOGGER.info(f"{client_ip}:{client_port} request video: {request.video} with model: {request.model}")

        self.camera = camera_server(model=request.model, video=request.video)
        while True:
            frame = self.camera.humanDetect()
            byteStream = helper.serializeTheImage(frame)
            img = image_pb2.image(data=byteStream)
            yield image_pb2.image_response(image_sent=img)
    
    def ack(self, request, context):
        if (request.req == "done video"):
            self.camera.close()
            logger._LOGGER.info("close video")

        return image_pb2.ack_response(rep="ok")

class grpcServer(protocolServer):
    def serve(self, address):
        logger._LOGGER.info("start a new server")

        myService = imageTranfer()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), maximum_concurrent_rpcs=2)
        image_pb2_grpc.add_image_tranferServicer_to_server(myService, server)

        server.add_insecure_port(address)
        server.start()
        server.wait_for_termination()


