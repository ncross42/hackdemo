#-*- coding: utf-8 -*-
import sqlite3
#import logging
#from logging.handlers import RotatingFileHandler

from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask import g
from flask import send_from_directory
#from flask import Markup
app = Flask(__name__, static_url_path='', template_folder='t')

DATABASE = 'db.sqlite'

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
    return render_template("test.html")

@app.route('/voted_list/')
def voted_list():
    f = open('s/votedlist.json')
#    js = json.loads(f.read())
    str = f.read();
    f.close()
    return str

@app.route('/voting/<name>/<value>')
def voting(name,value):

    return "name:" + name + ", value:" + value
@app.route('/get:_hier/')
def get_hier():
    return """
<div id="hier">
    <div class="citizen">
        <span>이희원</span>
        <div class="citizen">
            <span>대의원1</span>
            <div class="citizen"><span>시민1</span></div>
            <div class="citizen"><span>시민2</span></div>
        </div>
        <div class="citizen">
            <span>대의원2</span>
            <div class="citizen"><span>시민3</span></div>
            <div class="citizen"><span>시민4</span></div>
            <div class="citizen"><span>시민5</span></div>
            <div class="citizen"><span>시민6</span></div>
        </div>
        <div class="citizen">
            <span>대의원3</span>
            <div class="citizen"><span>시민7</span></div>
            <div class="citizen"><span>시민8</span></div>
            <div class="citizen"><span>시민9</span></div>
        </div>
    </div>
</div>"""



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
    app.run(host='0.0.0.0', port=80)
