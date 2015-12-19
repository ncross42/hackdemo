#-*- coding: utf-8 -*-
import sqlite3
import os
import json

#import logging
#from logging.handlers import RotatingFileHandler

from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask import g
from flask import send_from_directory
#from flask import Markup
app = Flask(__name__, static_url_path='', template_folder='t')

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
    return render_template("test.html")

@app.route('/user_list')
def user_list():
    try:
        c = g.db.cursor()
        c.execute('SELECT name FROM user ORDER BY name')
        rows = c.fetchall()
        tmp = json.dumps(rows).decode('unicode-escape').encode('utf8').replace('], [',',')
        return tmp[1:-1]
    except sqlite3.Error as e:
        return "An DB error occurred:", e.args[0]

@app.route('/issue_list')
def issue_list():
    try:
        result = []
        c = g.db.cursor()
        c.execute('SELECT * FROM issue ')
        rows = c.fetchall()
        for row in rows :
            result.append( {'issue_id':row[0], 'name':row[1]} )
        return json.dumps(result).decode('unicode-escape').encode('utf8')
    except sqlite3.Error as e:
        return "An DB error occurred:", e.args[0]

@app.route('/voted_list/')
def voted_list():
    voted_obj = {"votes":[]}
    voted_json = '{"votes":['
    try:
        c = g.db.cursor()
        # 's/votedlist.json'
        sql = "SELECT name, level, val FROM vote JOIN user USING (user_id)"
        # get old_val
        c.execute(sql)
        rows = c.fetchall()
        # execute new_val
        if rows is None :
            return sql
        else :
            voted_list = []
            for row in rows :
                voted_obj['votes'].append( {'name':row[0],'level':row[1],'value':row[2]} )
                voted_list.append ( '\n\t{ "name":"%s", "level":"%s", "value":"%s" }' % row )

            voted_json += ','.join(voted_list)
            voted_json += "\n]}"
            return voted_json
            #return json.dumps(voted_obj)

    except sqlite3.Error as e:
        return "An DB error occurred:", e.args[0]

@app.route('/voting')
def voting():

    user = request.args.get('name', '')
    value = request.args.get('value', '')
    #issue = request.args.get('subject', '')
    issue = ISSUE
    #app.logger.info('name: %s, value: %s, subject: %s', user, value, issue)

    new_val = int(value)
    try:
        c = g.db.cursor()
        # get issue
        c.execute("SELECT issue_id FROM issue WHERE name='%s'" % (issue) )
        row = c.fetchone()
        if row is None :
            raise Exception('Unkown Issue name : ' + issue )
        issue_id = row[0]
        # get user
        if user.isdigit() :
            user_id = int(user)
        else :
            c.execute("SELECT user_id FROM user WHERE name='%s'" % (user) )
            row = c.fetchone()
            if row is None :
                raise Exception('Unkown user name : ' + user )
            user_id = row[0]
        # get old_val
        c.execute("SELECT val FROM vote WHERE issue_id=%d AND user_id=%d" % (issue_id,user_id) )
        row = c.fetchone()
        # execute new_val
        if row is None :
            sql = "INSERT INTO vote (issue_id,user_id,val) VALUES (%d,%d,%d)" % (issue_id,user_id,new_val)
            c.execute(sql)
            g.db.commit()
        else :
            old_val = row[0]
            if new_val != old_val :
                sql = "UPDATE vote SET val=%d WHERE issue_id=%d AND user_id=%d" % (new_val,issue_id,user_id)
                c.execute(sql)
                g.db.commit()
    except sqlite3.Error as e:
        return "An DB error occurred:", e.args[0]
    return ""

@app.route('/hier_json/')
def hier_json(bJson=True):
    user_by_parent = {"max_level":2}
    try:
        c = g.db.cursor()
        for level in [0,1,2] :
            sql = 'SELECT parent, gr_name, name, user_id FROM user WHERE level=%d' % level
            c.execute(sql)
            rows = c.fetchall()
            for row in rows :
                parent = row[0]
                tmp = {'level':level,'team':row[1],'name':row[2],'user_id':row[3]}
                if parent in user_by_parent :
                    user_by_parent[parent].append(tmp)
                else :
                    user_by_parent[parent] = [tmp]
    except sqlite3.Error as e:
        return "An DB error occurred:", e.args[0]
    if bJson :
        return json.dumps(user_by_parent).decode('unicode-escape').encode('utf8')
    else :
        return user_by_parent

@app.route('/hier_json2/')
def hier_json2(bJson=True):
    data = [];
    try:
        c = g.db.cursor()
        for level in [0,1,2] :
            sql = 'SELECT parent, gr_name, name, user_id FROM user WHERE level=%d' % level
            c.execute(sql)
            rows = c.fetchall()
            user_by_parent = {}
            for row in rows :
                parent = str(row[0])
                tmp = {'team':row[1],'name':row[2],'user_id':row[3]}
                if parent in user_by_parent :
                    user_by_parent[parent].append(tmp)
                else :
                    user_by_parent[parent] = [tmp]
            data.append ( user_by_parent )
    except sqlite3.Error as e:
        return "An DB error occurred:", e.args[0]
    if bJson :
        return json.dumps(data).decode('unicode-escape').encode('utf8')
    else :
        return data

@app.route('/hier_html/')
def hier_html():

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

@app.route("/s/<path:p>")
def handle_static(p):
    return send_from_directory("s", filename=p)

if __name__ == "__main__":
    app.debug = True
    if  os.environ["USER"] in ['root','www-data','demo'] :
        app.run(host='0.0.0.0', port=80)
    else :
        app.run()
