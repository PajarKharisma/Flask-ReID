import cv2
ds_factor=0.6

import os
import imutils

class VideoCamera(object):
    def __init__(self, url=1):
        self.video = cv2.VideoCapture(url)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        image = imutils.resize(image, width=960)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()