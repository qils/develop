#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from mc import cache
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
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def add(cls, name, email):
        sql = ('insert into login_users(name, email) values(%s, %s)', )
        id_ = con.execute(sql, (name, email)).lastrowid
        # cls.clear_mc(id_)
        return cls.get(id_)

    @classmethod
    @cache(USER_KEY % '{id_}')
    def get(cls, id_):
        pass


class UserResource(Resource):
    @marshal_with(resource_fields)
    def get(self, name):
        pass

    def put(self, name):
        email = request.form.get('email')
        User.add(name, email)

        return {'ok': 'created'}, 201


api.add_resource(UserResource, '/api/<name>/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)

