#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from operator import or_
from functools import reduce
from ext import db
from flask_security import UserMixin, RoleMixin


class Permission(object):
    LOGIN = 0x01
    EDITOR = 0x02
    OPERATOR = 0x04
    ADMINSTER = 0xff

    Permission_Map = {
        LOGIN: ('login', 'login user'),
        EDITOR: ('editor', 'editor'),
        OPERATOR: ('operator', 'operator'),
        ADMINSTER: ('adminster', 'adminster')
    }

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    permissions = db.Column(db.Integer, default=Permission.LOGIN)
    description = db.Column(db.String(256))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=users_roles, backref=db.backref('users', lazy='dynamic'))

    def can(self, permission):
        if self.roles is None:
            return False

        all_perms = reduce(or_, map(lambda p: p.permissions, self.roles))
        return all_perms & permission == permission

    def can_admin(self):
        return self.can(Permission.ADMINSTER)
