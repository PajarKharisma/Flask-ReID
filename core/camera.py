import cv2
import os
import imutils

class VideoCamera(object):
    def __init__(self, url=1):
        self.video = cv2.VideoCapture(url)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        jpeg = None
        if success:
            curr_frame = self.video.get(cv2.CAP_PROP_POS_FRAMES)
            image = imutils.resize(image, width=960)
            ret, jpeg = cv2.imencode('.jpg', image)
            jpeg = jpeg.tobytes()

        return jpeg, success
