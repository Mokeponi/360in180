"""
Author: Remy D <remyd@civx.us>
Tim Duffy <tim@timduffy.me>
"""
from __future__ import division
import os
import threading

from flask import Flask, url_for, request, session, flash, redirect, g
from flask.ext.mako import MakoTemplates, render_template
#from flask.ext.login import LoginManage
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.sqlalchemy import SQLAlchemy
from .twitter import TwitterOAuth

import pymongo
import json
from bson import json_util
from bson import objectid

twitter = TwitterOAuth()
login_manager = LoginManager()

app = Flask(__name__, static_folder='../static', static_url_path='')
app.template_folder = "../templates"
app.config['MAKO_TRANSLATE_EXCEPTIONS'] = False
db = SQLAlchemy(app)
login_manager.init_app(app)
mako = MakoTemplates(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    token = db.Column(db.String(300))
    secret = db.Column(db.String(300))

    def __init__(self, username, token, secret):
        self.username = username
        self.token = token
        self.secret = secret

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@twitter.twitter_auth.tokengetter
def get_twitter_token():
  if current_user.is_authenticated():
        return (current_user.token, current_user.secret)
  else:
        return None

@app.before_request
def before_request():
    g.user = current_user

#Automatically include site config

@app.route('/getposts.json')
def getposts():

    # setup the connection based on enviornment
    if 'OPENSHIFT_MONGODB_DB_URL' in os.environ and 'OPENSHIFT_APP_NAME' in os.environ:
        uri = os.environ['OPENSHIFT_MONGODB_DB_URL']
        os.environ['OPENSHIFT_APP_NAME']
    else:
        uri = 'mongodb://localhost:27017/'
        dbname = 'maridian'

    conn = pymongo.Connection(uri)
    db = conn[dbname]

    posts = []
    success = True
    error = ''
    try:
        docs = db.posts.find()
        for d in docs:
            posts.append(d)
    except Exception, e:
        success = False
        error = str(e)

    response = {}
    response['success'] = success
    response['error'] = error
    response['apiversion'] = '0.0.1'
    response['posts'] = posts

    return json.dumps(response)

@app.route('/')
def index():
    return render_template('index.html', name='mako',
        user=current_user)

@app.route('/new')
#@login_required
def new():
    return render_template('editor.html', name='mako',
        user=current_user)

@app.route('/login')
def login():
  if current_user.is_authenticated():
      return redirect('/')
  return twitter.twitter_auth.authorize(callback=url_for('oauth_authorized',
      next=request.args.get('next') or request.referrer or None))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/oauth_authorized')
@twitter.twitter_auth.authorized_handler
def oauth_authorized(resp):
  next_url = request.args.get('next') or url_for('index')
  if resp is None:
        return redirect(next_url)

  this_account = User.query.filter_by(username = resp['screen_name']).first()
  if this_account is None:
        new_account = User(resp['screen_name'], resp['oauth_token'], resp['oauth_token_secret'])
        db.session.add(new_account)
        db.session.commit()
        login_user(new_account)
  else:
        login_user(this_account)

  return redirect(next_url)
