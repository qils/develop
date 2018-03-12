#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config

from werkzeug.wrappers import Response
from ext import db, manager
from models import LoginUser
from flask import Flask, request, render_template, url_for, redirect, jsonify
from flask_login import user_logged_in, login_user, login_required, current_user


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)
db.init_app(app)
manager.init_app(app)


class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)

        return super(JSONResponse, cls).force_type(response, environ)


app.response_class = JSONResponse


@app.before_first_request
def before_first_request():
    db.drop_all()
    db.create_all()


@user_logged_in.connect_via(app)
def login_users_count(sender, user, **extra):
    user.login_count += 1
    user.last_login_ip = request.remote_addr
    db.session.add(user)
    db.session.commit()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    name = request.form.get('name')
    passwd = request.form.get('passwd')

    if passwd == '123':
        user = LoginUser.query.filter_by(name=name).first()
        if not user:
            user = LoginUser(name=name)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for('protected'))
    else:
        return 'Password Bad'


@app.route('/protected/')
@login_required
def protected():
    user = current_user
    return {'login_count': user.login_count, 'last_login_ip': user.last_login_ip}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
