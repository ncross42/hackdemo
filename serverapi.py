#-*- coding: utf-8 -*-
import sqlite3
#import logging
#from logging.handlers import RotatingFileHandler

from flask import Flask
from flask import g
from flask import request
from flask import send_from_directory
#from flask import Markup
app = Flask(__name__, static_url_path='')

DATABASE = 'db.sqlite'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

#@app.after_request
#def after_request(response):
#    g.db.close()
#    return response

@app.route('/echo/')
def echo():
    return "You said: " + request.args.get('text', '')
@app.route('/')
def index():
    return 'Hello World'
@app.route('/something/')
def something():
    return 'something'
@app.route('/voting/')
@app.route('/voting/<name>,')
def user_id():
    return '유저'
    return '안건'



@app.route('/votedlist')
def print_something():
    user_id = request.args.get('user_id', '')
    bill_num = request.args.get('bill_num', '')
    value = request.args.get('value', '')
    app.logger.info('user_id: %s, bill_num: %s, value: %s', user_id, bill_num, value)
    return 'hello'

@app.route("/s/<path:p>")
def handle_static(p):
    return send_from_directory("s", filename=p)

if __name__ == "__main__":
    app.debug = True
    app.run()
