#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from log_module import log_module
from flask import Flask, Response, jsonify, request

from ext import db
from user import User

from flask_sqlalchemy import get_debug_queries


app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
app.config.from_object(config)
app.logger.handlers(log_module(app.config['LOG_LEVEL']))
db.init_app(app)


class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)

        return super(JSONResponse, cls).force_type(response, environ)


app.response_class = JSONResponse


with app.app_context():
    db.drop_all()
    db.create_all()


@app.route('/add_user/', methods=['POST'])
def add_user():
    name = request.form.get('name')
    user = User(name=name)

    db.session.add(user)
    db.session.commit()

    return {'name': user.name, 'id': user.id}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)