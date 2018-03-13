#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from flask import Flask
from ext import db, debug_tool_bar

from flask_script import Manager, Server, Shell
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)
debug_tool_bar.init_app(app)
manager = Manager(app)


def make_context_shell():
    return dict(db=db)


@manager.add_command('shell', Shell(make_context=make_context_shell))
@manager.add_command('runserver', Server(host='0.0.0.0', port=8888, use_debugger=True, use_reloader=True))
@app.route('/hello/')
def hello():
    return '<body>Hello, World</body>'


if __name__ == '__main__':
    manager.run()

