#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from flask import Flask, request, render_template

from ext import db
from models import PasteFile


app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
app.config.from_object(config)
db.init_app(app)


@app.after_request
def after_reqeust(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass

    return render_template('pastefile.html', **locals())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
