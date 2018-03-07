#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from flask import Flask, Response, request, jsonify

from user import User
from ext import db


app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
app.config.from_object(config)
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

    return {'add name': user.name}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)



