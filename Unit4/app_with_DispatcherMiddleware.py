#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from collections import OrderedDict
from flask import Flask, jsonify, render_template
from werkzeug.wrappers import Response
from werkzeug.wsgi import DispatcherMiddleware


app = Flask(__name__, template_folder='../templates', static_folder='../static')
json_page = Flask(__name__)


class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)

        return super(JSONResponse, cls).force_type(response, environ)


json_page.response_class = JSONResponse


@app.route('/')
def index():
    return render_template('macro.html')


@json_page.route('/page/')
def json_page():
    return {'ok': 1}


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/json': json_page})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)

