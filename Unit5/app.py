#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from flask import Flask, render_template


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)


@app.route('/login/')
def login():
    return render_template('sigin.html')
