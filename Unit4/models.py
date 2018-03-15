#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from ext import db, manager
from flask_login import UserMixin


@manager.user_loader
def user_loader(id):
    return LoginUser.query.filter_by(id=int(id)).first()


class LoginUser(UserMixin, db.Model):
    __tablename__ = 'login_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, default='maomao')
    login_count = db.Column(db.Integer, nullable=False, default=0)
    last_login_ip = db.Column(db.String(128), nullable=False, default='unknown')
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128))
    create_time = db.Column(db.DateTime())


