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


@app.route('/person-reid', methods=["GET", "POST"])
def index_file():
    if request.method == 'POST':
        if request.form['video_src'] == '1':
            url = request.form['url']
            return render_template('person-reid.html', url=url)
        elif request.form['video_src'] == '2':
            file = request.files['video']
            if 'video' not in request.files:
                flash('No file part')
            elif file.filename == '':
                flash('No selected file')
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template('person-reid.html', url=filename)
            else:
                flash('Extension not valid')
            return redirect(request.url)
        else:
            flash('Anda belum memilih sumber video')
            return redirect(request.url)
    else:
        return render_template('person-reid.html')

def gen(camera):
    while True:
        frame, success = camera.get_frame()
        if success:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            del camera
            break

@app.route('/video_feed/<filename>')
def video_feed(filename):
    if len(filename) > 1:
        url_video = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        url_video = int(filename)
    return Response(gen(VideoCamera(url_video)), mimetype='multipart/x-mixed-replace; boundary=frame')