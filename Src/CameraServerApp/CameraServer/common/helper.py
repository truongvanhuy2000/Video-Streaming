import cv2
import numpy as np

def deserializeTheImage(byte):
    im_arr = np.frombuffer(byte, dtype=np.uint8)  # im_arr is one-dim Numpy array
    return cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

def serializeTheImage(image):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
    img = cv2.imencode('.jpeg', image, encode_param)[1].tobytes()
    return img

