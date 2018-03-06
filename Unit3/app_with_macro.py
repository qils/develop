#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from datetime import datetime
from flask import Flask, render_template


app = Flask(__name__, template_folder='../templates/', static_folder='../static/')


@app.route('/hello/')
def hello():
    return render_template('index.html', alist=[1, 2, 3], time=datetime.now())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
