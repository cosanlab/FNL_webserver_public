"""
Routing for API calls; expand with additional fields as nescessary
"""

from flask import Flask, request, render_template, jsonify, abort, send_file, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, select, inspect, MetaData, Table, Column
from os import system
from functools import wraps

from models import ep1, ep2, ep3, ep4, ep1_annotations
from app import app, google, oauth, db, e, api_key
# from ffmpeg_shell import *

# app.config.update(
#     CELERY_BROKER_URL='redis://localhost',
#     CELERY_BACKEND='redis://localhost'
# )

# celery = make_celery(app)

"Old function used to prepare SQLAlchemy output to be JSON serialized; not used"

def serialize(_query):
    #Formats SQLAlchemy output to be JSON readable
    #d = dictionary written to per row
    #D = dictionary d is written to each time, then reset
    #Master = dictionary of dictionaries; the id Key (int, unique from database) from D is used as the Key for the dictionary D entry in Master
    Master = {}
    D = {}
    x = 0
    for u in _query:
        d = u.__dict__
        D = {}
        for n in d.keys():
            if n != '_sa_instance_state':
                D[n] = d[n]
        x = d['id']
        Master[x] = D
    return Master

"Old time parsing function; can be removed"
# def datetimer(sqry):
#     for j in sqry.keys():
#         for n in sqry[j].keys():
#             if n == 'timeend' or n == 'timestart':
#                 # print n
#                 sqry[j][n] = "%s"%sqry[j][n]
#                 # print sqry[j][n]
#     return (sqry)

"Used for parsing times; allows the processing of timestamps of HH:MM:SS.SSS, MM:SS.SSS, or SS.SSS"
"Expects one of these values"
def time_parse(time):
    #expects format of '00:00:00'
    l=[n for n in time.split(':')]
    if len(l) == 3:
        for n in range(len(l)):
            l[n] = eval(l[n])
        l[2]+=l[1]*60+l[0]*3600
        return l[2]
    elif len(l) == 2:
        for n in range(len(l)):
            l[n] = eval(l[n])
        l[1]+=l[0]*60
        return l[1]
    elif len(l) == 1:
        l[0] = eval(l[0])
        return l[0]

'===================================================================='

"Creates a decorator that can be applied to require the API key on a route"
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == api_key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

"Not currently called; intended to allow someone to view the authorized users"
# def user_list():
#     emails = []
#     conn = e.connect()
#     qry = conn.execute("SELECT email FROM user")
#     user_email = [dict(zip(tuple (qry.keys()) ,i)) for i in qry.cursor]
#     for n in range(len(user_email)):
#         for a in user_email[n].keys():
#             emails.append(user_email[n][a])
#     return emails

'===================================================================='

"FNL call; should be expandable to fulfill most SQL calls"
"Hierarchy based around:"
"tv.cosanlab.com/api/<study>/<episode>/?key=<key>&<query>"
"Should be expandable off of this; with more complex functions, adding different componenets to the URL may be necessary"
@app.route('/api/FNL/<string:table>/')
@require_appkey
def selectFromFNL_ROUTE(table):
    table = table
    start = request.args.get('start')
    if start == None:
        start = '00:00:00.0'
    end = request.args.get('end')
    if end == None:
        end = '01:00:00.0'

    conn = e.connect()
    # qry = conn.execute("SELECT dialogue, timestart FROM %s WHERE timestart BETWEEN ? and ?"%episode, start, end)
    # if table == ep1 or table == ep2 or table == ep3 or table == ep4:
    #     qry = conn.execute("SELECT dialogue, timestart FROM %s WHERE timestart BETWEEN '%s' and '%s'"%(table, start, end))
    # elif table == ep1_annotations:
    #     qry = conn.execute("SELECT * FROM %s WHERE timestart BETWEEN '%s' and '%s' or timeend BETWEEN '%s' and '%s' "%(table, start, end, start, end))
    # else:
    qry = conn.execute("SELECT * FROM %s WHERE timestart BETWEEN '%s' and '%s' or timeend BETWEEN '%s' and '%s'"%(table, start, end, start, end))
    return jsonify({'data': [dict(zip(tuple (qry.keys()) ,i)) for i in qry.cursor]})

"""Old routing for API; """
# @app.route('/api/FNL/<string:episode>/')
# @require_appkey
# def selectFromFNL_ROUTE(episode):
#     episode = episode
#     start = request.args.get('start')
#     if start == None:
#         start = '00:00:00.0'
#     end = request.args.get('end')
#     if end == None:
#         end = '01:00:00.0'

#     conn = e.connect()
#     # qry = conn.execute("SELECT dialogue, timestart FROM %s WHERE timestart BETWEEN ? and ?"%episode, start, end)
#     qry = conn.execute("SELECT dialogue, timestart FROM %s WHERE timestart BETWEEN '%s' and '%s'"%(episode, start, end))
#     return jsonify({'data': [dict(zip(tuple (qry.keys()) ,i)) for i in qry.cursor]})

'=================================================================='

"Slicing; not currently working"
@app.route('/slice/<string:episode>/')
def slice(episode):
    episode = episode
    time = request.args.get('time')
    image = framegrab(episode, time)
    return send_file(image, mimetype = 'image/gif')
