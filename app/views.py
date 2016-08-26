#views.py

"""
Main routing for the app
Issue when routing to the homepage when the user is logged in; maybe switch the routings for the oauth?
"""

from flask import Flask, request, render_template, jsonify, abort, send_file, redirect, url_for, session
from flask_oauthlib.client import OAuth
from functools import wraps

from app import app, google, e
from login import Permissions

'================================================================================='

permissions = Permissions()

def user_list():
    emails = []
    conn = e.connect()
    qry = conn.execute("SELECT email FROM user")
    user_email = [dict(zip(tuple (qry.keys()) ,i)) for i in qry.cursor]
    for n in range(len(user_email)):
        for a in user_email[n].keys():
            emails.append(user_email[n][a])
    return emails

user_list = user_list()

#require user to be approved to access the data
def require_login(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        emails = user_list
        if 'google_token' in session:
            me = google.get('userinfo')
            user = {"data": me.data}
            if user['data']['email'] in emails:
                return view_function(*args, **kwargs)
        abort(401)
    return decorated_function

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

'================================================================================='
"OAuth Routing for Google"

@app.errorhandler(502)
def bad_gateway(e):
    permissions.logout_user()
    return render_template('index.html',login=login, name=name, authorized=authorized)

@app.route('/')
def index():
    permissions.update_user()
    login,name,authorized = permissions.validate_user()
    if 'google_token' in session:
        try:
            login,name,authorized = permissions.validate_user()
            return render_template('index.html', login=login, name=name, authorized=authorized)
        except:
            session.pop('google_token', None)
            permissions.logout_user()
            permissions.update_user()
            # return redirect(url_for('login'))
            login,name,authorized = permissions.validate_user()
            return render_template('index.html', login=login, name=name, authorized=authorized)
        # return redirect(url_for('logout'))
    # try
    # session.pop('google_token', None)
    permissions.logout_user()
    permissions.update_user()
    # return redirect(url_for('login'))
    login,name,authorized = permissions.validate_user()
    return render_template('index.html', login=login, name=name, authorized=authorized)
    # except:
    #     permissions.logout_user()
    #     permissions.update_user()
    #     # return redirect(url_for('login'))
    #     login,name,authorized = permissions.validate_user()
    #     return render_template('index.html', login=login, name=name, authorized=authorized)
#     if 'google_token' in session:
#         me = google.get('userinfo')
#         user = {"data": me.data}
#         name = user['data']['given_name']
#         # return jsonify({"data": me.data})
#         emails = user_list
#         permissions.update_user()
#         login,name,authorized = permissions.validate_user()
#         if user['data']['email'] in emails:
#             return render_template('index.html', login=True, name=name, authorized=True)
#         else:
#             # return render_template('index.html', login=True, name=name, authorized=False)
#         return render_template('index.html',  timestart=timestart, name=name, authorized=authorized)
# #        except:
# #            render_template('index.html', login=True)
#     return render_template('index.html', login=False)

@app.route('/login/')
def login():
    if 'google_token' in session:
        session.pop('google_token', None)
        permissions.logout_user()
        permissions.update_user()
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout/')
def logout():
    session.pop('google_token', None)
    permissions.logout_user()
    return redirect(url_for('index'))


@app.route('/login/authorized/')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    # return jsonify({"data": me.data})
    permissions.update_user()
    return redirect(url_for('index'))

"Creating a logged in decorator"
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

'================================================================================='

#streaming front end; renders HTML
@app.route('/streaming/ep1/<string:timestart>/')
@require_login
def video_html_render(timestart):
    timestart=time_parse(timestart)
    # login,name,authorized = validate_login()
    login,name,authorized = permissions.validate_user()
    return render_template('video.html', timestart=timestart, name=name, authorized=authorized)

#streaming front end; renders HTML
@app.route('/streaming/ep1/')
@require_login
def slice_render():
    # login,name,authorized = validate_login()
    login,name,authorized = permissions.validate_user()
    return render_template('video.html', login=login, name=name, authorized=authorized)

#.webm video serve; sends the video file when called
#@app.route('/streaming/FNL_Videos/FNL_01.mp4')
@app.route('/stream/ep1/FNL_01_640x360_h264_med.webm')
def video_serve_ep1_webm():
    # return send_file('templates/FNL_01_640x360_h264_med.webm', mimetype='video/webm')
    return send_file('static/FNL_01_640x360_h264_med.webm', mimetype='video/webm')

'================================================================================='

"TEST Hello World"
@app.route('/test/', methods=['GET'])
def test():
        return render_template('base.html')
