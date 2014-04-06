"""
Author: Remy D <remyd@civx.us>
        Tim Duffy <tim@timduffy.me>
"""
from __future__ import division
import os
import threading

from flask import Flask
from flask.ext.mako import MakoTemplates, render_template

app = Flask(__name__)
app.template_folder = "../templates"
mako = MakoTemplates(app)


# Automatically include site config

@app.route('/')
def index():
    return render_template('index.html', name='mako')
