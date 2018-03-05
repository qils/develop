#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from flask import Flask, jsonify
from werkzeug.wrappers import Response


app = Flask(__name__, template_folder='../templates/', static_folder='../static/')


class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JSONResponse, cls).force_type(response, environ)


app.response_class = JSONResponse


@app.route('/custom_headers/')
def custom_headers():
    return {'headers': [1, 2, 3]}, 201, [('X-Request-Id', 100)]


@app.route('/hello_world/')
def hello_world():
    return {'message': 'Hello, world'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
