import os
import sys
from flask import render_template, request, redirect, Response, flash, url_for
from werkzeug.utils import secure_filename

from app import app

from core.camera import VideoCamera

UPLOAD_FOLDER = 'temp/'
ALLOWED_EXTENSIONS = {'mp4', 'avi', '3gp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/reid-list', methods=["GET"])
def index_list():
    if request.method == 'GET':
        img_list = os.listdir('static/list/')
        results = []
        for index, img in enumerate(img_list):
            data = {
                'img' : img,
                'id' : 'person-{}'.format(index+1)
            }
            results.append(data)
            
        return render_template('reid-list.html', results=results)
    else:
        return redirect('/home')