from flask import Flask
# from flask_mysqldb import MySQL, MySQLdb
import os
import sys

app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'cctv'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)
app.secret_key = os.urandom(24)

import views

if __name__ == "__main__":
    app.run(debug=True)

# os.system("clear-cache.sh")