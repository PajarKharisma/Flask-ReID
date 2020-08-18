import cv2
ds_factor=0.6

import os

class VideoCamera(object):
    def __init__(self, url=1):
        self.video = cv2.VideoCapture(url)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()