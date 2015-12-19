#-*- coding: utf-8 -*-
import sqlite3
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask import g
from flask import request
from flask import Markup
app = Flask(__name__)

DATABASE = '/Users/dididy/hello.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    return 'Hello World'
@app.route('/something/')
def something():
    return 'something'
@app.route('/voting/')
@app.route('/voting/<user_id>')
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
if __name__ == "__main__":
    app.debug = True
    app.run()
