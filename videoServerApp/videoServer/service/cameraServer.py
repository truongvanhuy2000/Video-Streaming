from videoServer.common import helper
from videoServer.aiModel import modelProvider
import cv2

class camera_server():
    def __init__(self, video, model) -> None:
        # dir = '/home/huy/Videos/' + video +'.mp4'
        dir = 'videoServer/resources/' + video + '.mp4'
        self.cap = cv2.VideoCapture(dir)
        # self.AImodel = modelProvider.getModel(model)
    
    def humanDetect(self):
        # Display the resulting frame
        # initialize the HOG descriptor
        try:
            ret, frame = self.cap.read()
        except:
            print("something wrong here")
        if ret == False:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        # self.AImodel.detect(frame)
        return frame
    
    def isOpen(self) -> bool:
        return self.cap.isOpened()
    
    def close(self):
        self.cap.release()