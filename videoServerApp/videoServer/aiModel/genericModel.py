from videoServer.aiModel.model import model
import cv2

class genericModel(model):
    def __init__(self) -> None:
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self, frame):
        (humans, _) = self.hog.detectMultiScale(frame, winStride=(10, 10), padding=(32, 32), scale=1.1)
        # loop over all detected humans
        for (x, y, w, h) in humans:
            pad_w, pad_h = int(0.15 * w), int(0.01 * h)
            cv2.rectangle(frame, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), 2)
        return frame