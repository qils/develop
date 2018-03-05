#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from flask import Flask, jsonify, g, abort
from werkzeug.wrappers import Response
from flask.views import MethodView

app = Flask(__name__, template_folder='../templates/', static_folder='../static/')


class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JSONResponse, cls).force_type(response, environ)


app.response_class = JSONResponse


class UserView(MethodView):
    def get(self):
        return {'username': 'fake', 'avator': 'http://baidu.com'}

    def post(self):
        return 'Unsupported'


def user_required(func):
    def wrapper(*args, **kwargs):
        if not g.user:
            abort(403)

        return func(*args, **kwargs)
    return wrapper

view = user_required(UserView.as_view('userview'))
app.add_url_rule('/user/', view_func=view)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)


