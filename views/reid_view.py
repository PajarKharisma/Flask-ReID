import os
import sys
from flask import render_template, request, redirect, Response, flash, url_for
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL, MySQLdb

from app import app
from app import mysql

from core.camera import VideoCamera

UPLOAD_FOLDER = 'temp/'
ALLOWED_EXTENSIONS = {'mp4', 'avi', '3gp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/reid-analyze', methods=["GET", "POST"])
def index_file():
    data= {}
    if request.method == 'POST':
        if request.form['video_src'] == '1':
            filename = request.form['url']
        elif request.form['video_src'] == '2':
            file = request.files['video']
            if 'video' not in request.files:
                flash('No file part')
            elif file.filename == '':
                flash('No selected file')
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Extension not valid')
            return redirect(request.url)
        elif request.form['video_src'] == '3':
            filename = request.form['cctv']
        else:
            flash('Anda belum memilih sumber video')
            return redirect(request.url)
        
        data['input_type'] = request.form['video_src']
        data['filename'] = filename
        
    # baca daftar cctv dari database
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT cctvId, cctvName FROM ref_cctv")
    data['cctv_ids'] = cur.fetchall()
    cur.close()
    return render_template('reid-person.html', data=data)

def gen(camera):
    while True:
        frame, success = camera.get_frame()
        if success:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            del camera
            break

@app.route('/video_feed/<input_type>/<filename>')
def video_feed(input_type, filename):
    if int(input_type) == 1:
        url_video = int(filename)
    elif int(input_type) == 2:
        url_video = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM ref_cctv WHERE cctvId={}".format(int(filename)))
        cctv_data = cur.fetchone()
        cur.close()
        if cctv_data['cctvUrl'] == '':
            # rtsp://admin:adminYKQFNH@169.254.108.121
            url_video = '{}://{}:{}@{}:{}'.format(
                cctv_data['cctvType'],
                cctv_data['cctvUser'],
                cctv_data['cctvPassword'],
                cctv_data['cctvIp'],
                cctv_data['cctvPort']
            )
        else:
            url_video = cctv_data['cctvUrl']
    
    return Response(gen(VideoCamera(url_video)), mimetype='multipart/x-mixed-replace; boundary=frame')