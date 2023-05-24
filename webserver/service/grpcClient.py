import grpc
from webserver.proto import image_pb2, image_pb2_grpc

import cv2
import time

from webserver.common.helper import deserializeTheImage
def request(video, model, port):
    channel_opt = [
            ("grpc.so_reuseport", 1),
            ("grpc.use_local_subchannel_pool", 1)
        ]
    with grpc.insecure_channel('localhost:{}'.format(port), options=channel_opt) as channel:
        stub = image_pb2_grpc.image_tranferStub(channel=channel)
        response = stub.send_me_image(image_pb2.image_request(model=model, video=video))
        try:
            for img in response:
                frame = deserializeTheImage(img.image_sent.data)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                # Yield the frame in byte format
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            print("video done")
        stub.ack(image_pb2.ack_request(req="done video"))

            