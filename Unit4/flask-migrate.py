#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from flask import Flask
from ext import db
from models import LoginUser

from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, LoginUser=LoginUser)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host='0.0.0.0', port=8888, use_reloader=True, use_debugger=True))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
