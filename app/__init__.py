import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, select, inspect, MetaData, Table, Column
from flask_oauthlib.client import OAuth
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager

"Must set the basedir for whatever your local system is; comment it out before pushing"
# basedir = os.path.abspath(os.path.dirname(__file__))
# basedir = '/home/cosanlab/tv.cosanlab.com'
# basedir = '/Users/lukechang/Github/FNL_Web'
basedir = '../'

"importing the keys; requires the above path specification"
import imp
keypath = imp.load_source('keys', os.path.join(basedir,'keys','keys.py'))
keys = keypath.Keys()


"setting up the keys and dependencies with the app instance"
app = Flask(__name__)
app.secret_key = keys.secret_key
app.debug = True
oauth = OAuth(app)
db = SQLAlchemy(app)
manager = Manager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = keys.db_name_from_keys
e = create_engine(keys.db_name_from_keys)
api_key = keys.api_key

bootstrap = Bootstrap(app)

"Oauth configuration"
app.config['GOOGLE_ID'] = keys.GOOGLE_ID
app.config['GOOGLE_SECRET'] = keys.GOOGLE_SECRET

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


import models

"importing the routing scripts"
"NOTE: must disable when initializing the database"
import api, views
