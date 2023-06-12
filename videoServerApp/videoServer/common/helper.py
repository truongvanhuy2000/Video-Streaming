import cv2
import pybase64
import numpy as np
import socket


# def deserializeTheImage(byte):
#     jpg_original = pybase64.b64decode(byte)
#     im_arr = np.frombuffer(jpg_original, dtype=np.uint8)  # im_arr is one-dim Numpy array
#     return cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

# def serializeTheImage(image):
#     img = cv2.imencode('.jpeg', image)[1]
#     jpg_as_text = pybase64.b64encode(img)
#     return jpg_as_text

def deserializeTheImage(byte):
    im_arr = np.frombuffer(byte, dtype=np.uint8)  # im_arr is one-dim Numpy array
    return cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

def serializeTheImage(image):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
    img = cv2.imencode('.jpeg', image, encode_param)[1].tobytes()
    return img

# to check if socket still open
def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        return False
    return False

