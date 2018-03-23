#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import ast
import datetime
from ext import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
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


class PasteFile(db.Model):
    __tablename__ = 'paste_file'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, uploaded_time=None):
        self.name = name
        self.uploaded_time = datetime.datetime.now() if not uploaded_time else uploaded_time

    def to_dict(self):
        print vars(self)
        adict = {k: v for k, v in vars(self).items() if not k.startswith('_')}
        adict['uploaded_time'] = adict['uploaded_time'].strftime('%Y%m%dT%H%M%S.%f')
        return str(adict)

    @classmethod
    def from_dict(cls, data):
        data = ast.literal_eval(data)
        id = data.pop('id')
        data['uploaded_time'] = datetime.datetime.strptime(data['uploaded_time'], '%Y%m%dT%H%M%S.%f')
        p = cls(**data)
        p.id = id
        return p
