import grpc
import cv2
import asyncio

from webServer.proto import image_pb2, image_pb2_grpc
from webServer.common.helper import deserializeTheImage
from webServer.transportation.protocol.clientProtocol import clientProtocol
from webServer.common import logger


class grpcClient(clientProtocol):
    def __init__(self, addr) -> None:
        channel_opt = [("grpc.so_reuseport", 1), ("grpc.use_local_subchannel_pool", 1)]

        logger._LOGGER.info(f"Connect to GRPC server: {addr}")

        self.channel = grpc.insecure_channel(addr, options=channel_opt)
        self.stub = image_pb2_grpc.image_tranferStub(channel=self.channel)
        asyncio.run(self.waitForServer())

    async def waitForServer(self):
        while True:
            try:
                rep = await self.stub.are_you_ready(image_pb2.ready_request(req="READY"))
                logger._LOGGER.info(f"Server response is {rep.rep}")
                if rep.rep == "READY":
                    break
            except:
                continue

    def request(self, video, model):            
        logger._LOGGER.info(f"Start Requesting image")
        response = self.stub.send_me_image(image_pb2.image_request(model=model, video=video))
        try:
            for img in response:
                frame = deserializeTheImage(img.image_sent.data)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                # Yield the frame in byte format
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            response.cancel()
            logger._LOGGER.info("Done Streaming")
            self.stub.ack(image_pb2.ack_request(req="done video"))
            self.channel.close()

    def response(self):
        pass


            