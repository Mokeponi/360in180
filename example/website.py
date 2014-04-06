import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask
from flask import render_template
from flask import request

import json
import datetime

app = Flask(__name__, static_folder='static', static_url_path='')
app.template_folder = "."
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':

    print "Web App Starting ..."

    host = '0.0.0.0'
    port = 8080

    app.run(host=host, port=port)
