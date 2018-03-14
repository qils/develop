#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from decorator import permission_required, admin_required
from flask import Flask
from ext import db
from modules import User, Role, Permission

from flask_script import Manager, Server, Shell
from flask_security import SQLAlchemyUserDatastore, Security, login_required
from flask_security.forms import LoginForm


app = Flask(__name__, template_folder='/root/web_develop/venv/lib/python2.7/site-packages/flask_security/security/templates',
            static_folder='../../static')
app.config.from_object(config)
db.init_app(app)
manager = Manager(app)


def make_context_shell():
    return dict(app=app, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_context_shell))
manager.add_command('runserver', Server(host='0.0.0.0', port=8888, use_debugger=True, use_reloader=True))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=LoginForm)


@security.login_context_processor
def login_context_processor():
    print 'Login'
    return {}


@app.before_first_request
def create_user():
    db.drop_all()
    db.create_all()

    for permissions, (name, description) in Permission.Permission_Map.items():
        user_datastore.find_or_create_role(permissions=permissions, name=name, description=description)

    for email, password, permissions in (('maomao@163.com', '123', (Permission.LOGIN, Permission.EDITOR)),
                                         ('admin@163.com', '123', (Permission.ADMINSTER, ))):
        user_datastore.create_user(email=email, password=password)

        for permission in permissions:
            user_datastore.add_role_to_user(email, Permission.Permission_Map[permission][0])

    db.session.commit()


@app.route('/')
@login_required
@permission_required(Permission.LOGIN)
def index():
    return 'hi, index'


@app.route('/admin/')
@login_required
@admin_required
def admin():
    return 'Admin'


if __name__ == '__main__':
    manager.run()


