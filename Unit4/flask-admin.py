#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
import os.path
from ext import db, login_manager
from flask import Flask, url_for, redirect
from models import LoginUser

from flask_login import login_user, logout_user, current_user
from flask_script import Manager, Server, Shell
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.base import MenuLink, BaseView, expose


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)
db.init_app(app)
login_manager.init_app(app)
manager = Manager(app)


@app.before_first_request
def before_first_request():
    db.drop_all()
    db.create_all()

    user = LoginUser(name='maomao1', email='maomao1@163.com', password='123')
    db.session.add(user)
    db.session.commit()


def make_context_shell():
    return dict(app=app, LoginUser=LoginUser)


manager.add_command('shell', Shell(make_context=make_context_shell))
manager.add_command('runserver', Server(host='0.0.0.0', port=8888, use_debugger=True, use_reloader=True))


@app.route('/')
def index():
    return '<a href="/admin/">点击进入管理后台</a>'


@app.route('/login/')
def login():
    user = LoginUser.query.filter_by(name='maomao1').first()
    login_user(user)

    return redirect(url_for('admin.index'))


@app.route('/logout/')
def logout():
    logout_user()

    return redirect(url_for('admin.index'))

admin = Admin(app, name=u'站点管理', template_mode='bootstrap3')
admin.add_view(ModelView(LoginUser, db.session))

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static')
admin.add_view(FileAdmin(path, '/static/', name=u'静态文件管理'))

admin.add_link(MenuLink(name='首页', url='/'))
admin.add_link(MenuLink(name='Google', url='http://www.google.com', category=u'其它连接'))
admin.add_link(MenuLink(name=u'百度', url='http://www.baidu.com', category=u'其它连接'))


if __name__ == '__main__':
    manager.run()

