import cv2

class videoProcessor():
    def __init__(self):
        pass
    
    def drawBoundingBox(self, frame, coordinates):
        
        for (x,y,w,h) in coordinates:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
        
        return frame