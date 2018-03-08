#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import random
import config
from flask import Flask, g, render_template

from ext import db
from user import User


app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
app.config.from_object(config)
db.init_app(app)


def get_current_user():
    users = User.query.all()
    return random.choice(users)


@app.before_first_request
def set_up():
    db.drop_all()
    db.create_all()

    fake_data = [User(name=username) for username in ('maomao1', 'maomao2', 'maomao3')]
    db.session.add_all(fake_data)
    db.session.commit()


@app.before_request
def before_request():
    g.user = get_current_user()


@app.teardown_appcontext
def tearown(exc=None):
    if not exc:
        db.session.commit()
    else:
        db.session.rollback()
    db.session.remove()
    g.user = None


@app.context_processor
def context_processor():
    return {'enumerate': enumerate, 'current_user': g.user}


@app.errorhandler(400)
def errorhandler(error):
    return 'This page is not exist', 404


@app.template_filter('capitalize')
def template_filte(s):
    return s.capitalize()


@app.route('/user/')
def user():
    users = User.query.all()
    return render_template('user.html', users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
