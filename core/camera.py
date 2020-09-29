import cv2
import os
import imutils
import json

import core.kardinal as krd

class VideoCamera(object):
    def __init__(self, url=1, analyze_type='reid', disable_bb=0):
        self.video = cv2.VideoCapture(url)
        self.kardinal = krd.Kardinal()
        self.analyze_type = analyze_type
        self.disable_bb = int(disable_bb)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        jpeg = None
        if success:
            curr_frame = self.video.get(cv2.CAP_PROP_POS_FRAMES)
            image = imutils.resize(image, width=640)

            if self.disable_bb == 0 and self.analyze_type == 'reid':
                image = self.kardinal.detected(image, curr_frame)
            elif self.disable_bb == 0 and self.analyze_type == 'counting':
                image = self.kardinal.people_counting(image, curr_frame-1)
            
            ret, jpeg = cv2.imencode('.jpg', image)
            jpeg = jpeg.tobytes()

        return jpeg, success
