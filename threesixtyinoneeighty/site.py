"""
Author: Remy D <remyd@civx.us>
        Tim Duffy <tim@timduffy.me>
"""
from __future__ import division
import os
import threading

from flask import Flask, url_for, request, session, flash, redirect
from flask.ext.mako import MakoTemplates, render_template
from .twitter import TwitterOAuth
twitter = TwitterOAuth()

app = Flask(__name__, static_folder='../static', static_url_path='')
app.template_folder = "../templates"
mako = MakoTemplates(app)


# Automatically include site config

@app.route('/')
def index():
    return render_template('index.html', name='mako',
        twitter_user=session['twitter_user'] if 'twitter_user' in session else None
    )

@app.route('/new')
def new():
    return render_template('editor.html', name='mako')

@app.route('/login')
def login():
    return twitter.twitter_auth.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))

@app.route('/oauth_authorized')
@twitter.twitter_auth.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

