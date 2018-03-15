#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from flask import Flask
from werkzeug.contrib.profiler import ProfilerMiddleware


app = Flask(__name__)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='/tmp')


@app.route('/test/<int:id_>/')
def hello(id_):
    print type(id_)
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
