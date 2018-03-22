#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from mc import cache, mc
from flask import Flask, request
from sqlalchemy import create_engine

from flask_restful import Api, marshal_with, fields, Resource


app = Flask(__name__, template_folder='../../templates', static_folder='../../static')
app.config.from_object(config)
api = Api(app)
con = create_engine(app.config['DB_URI']).connect()
USER_KEY = 'web_develop:users:%s'


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}


class User(object):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    @classmethod
    def add(cls, name, email):
        sql = ('insert into login_users(name, email) ' 
               'values(%s, %s)')
        id_ = con.execute(sql, (name, email)).lastrowid
        cls.clear_mc(id_)
        return cls.get(id_)

    @classmethod
    @cache(USER_KEY % '{id_}')
    def get(cls, id_):
        if not id_:
            return None

        row = con.execute('select id, name, email from login_users where id=%s', id_).fetchone()
        print row
        return cls(*row) if row else None

    @classmethod
    def get_user_by_id(cls, id):
        return cls.get(id)

    def delete(self):
        con.execute('delete from login_users where id=%s', self.id)
        self.clear_mc(self.id)

    @classmethod
    def clear_mc(cls, id):
        mc.delete(USER_KEY % id)


class UserResource(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        user = User.get_user_by_id(id)
        return user

    def put(self, name):        # 添加User实例
        email = request.form.get('email')
        User.add(name, email)

        return {'ok': 'created'}, 201

    def delete(self, id):
        user = User.get_user_by_id(id)
        if user:
            user.delete()

        return {'OK': 0}


api.add_resource(UserResource, '/api/<name>/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
