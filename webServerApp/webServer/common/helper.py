import cv2
import pybase64
import numpy as np

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
    img = cv2.imencode('.jpeg', image)[1].tobytes()
    return img