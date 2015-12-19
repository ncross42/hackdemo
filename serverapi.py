#-*- coding: utf-8 -*-
import sqlite3
#import logging
#from logging.handlers import RotatingFileHandler

from flask import Flask, session, redirect, url_for, escape, request
from flask import g
from flask import send_from_directory
#from flask import Markup
app = Flask(__name__, static_url_path='')

DATABASE = 'db.sqlite'
ISSUE = "담배값 1만원 인상"

@app.before_request
def before_request():
    g.db = sqlite3.connect(DATABASE)

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'Hello World'
@app.route('/voted_list/')
def voted_list():
    f = open('s/votedlist.json')
#    js = json.loads(f.read())
    str = f.read();
    f.close()
    return str

@app.route('/voting/<user_name>/<value>')
def voting(user_name,value,issue=ISSUE):
    new_val = int(value)
    try:
        c = g.db.cursor()
        issue_id = c.fetchone("SELECT issue_id FROM issue WHERE name = '" + issue +"'")
        if issue_id == None :
            raise Exception('Unkown Issue name : ' + issue )
        user_id = c.fetchone("SELECT user_id FROM user WHERE name = '" + user_name +"'")
        if user_id == None :
            raise Exception('Unkown User name : ' + name )
        old_val = c.fetchone("SELECT val FROM vote WHERE issue_id = "+issue_id+" AND user_id = "+user_id)
        if old_val == None :
            sql = "INSERT INTO vote (issue_id,user_id,val) VALUES (%d,%d,%d)" % (issue_id,user_id,new_val)
        elif new_val != old_val :
            sql = "UPDATE vote SET val=%d WHERE issue_id=%d AND user_id=%d" % (new_val,issue_id,user_id)
    except sqlite3.Error as e:
        return "An DB error occurred:", e.args[0]
    return ""

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
    #app.run(host='0.0.0.0', port=80)
    app.run()
