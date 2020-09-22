import os
import sys
import json
from flask import render_template, request, redirect, Response, flash, url_for


from app import app

CONFIG_FILE = 'static/config.json'

@app.route('/reid-config', methods=["GET", "POST"])
def index_config():
    if request.method == 'GET':
        return render_template('reid-config.html')
    else:
        with open(CONFIG_FILE) as json_file:
            data = json.load(json_file)
        if request.form['config_mode'] != '0':
            data['mode'] = int(request.form['config_mode'])
            flash('Data saved')
        else:
            flash('Data saved as default')

        with open(CONFIG_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)
        return redirect(request.url)
