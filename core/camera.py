import cv2
import os
import imutils
import json

import core.kardinal as krd

CONFIG_FILE = 'static/config.json'

class VideoCamera(object):
    def __init__(self, url=1):
        self.video = cv2.VideoCapture(url)
        self.kardinal = krd.Kardinal()
        with open(CONFIG_FILE) as json_file:
            self.config = json.load(json_file)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        jpeg = None
        if success:
            curr_frame = self.video.get(cv2.CAP_PROP_POS_FRAMES)
            image = imutils.resize(image, width=640)

            if self.config['mode'] == 2:
                image = self.kardinal.detected(image, curr_frame)
            elif self.config['mode'] == 3:
                image = self.kardinal.people_counting(image, curr_frame-1)
            
            ret, jpeg = cv2.imencode('.jpg', image)
            jpeg = jpeg.tobytes()

        return jpeg, success
