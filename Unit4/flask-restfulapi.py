#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from flask import Flask, request
from ext import db
from models import LoginUser

from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, Shell, Server
from flask_restful import Resource, marshal_with, reqparse, fields, Api


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
manager = Manager(app)


@app.before_first_request
def before_first_request():
    db.drop_all()
    db.create_all()


def make_context_shell():
    return dict(app=app, LoginUser=LoginUser)


manager.add_command('shell', Shell(make_context=make_context_shell))
manager.add_command('runserver', Server(host='0.0.0.0', port=8888, use_reloader=True, use_debugger=True))
manager.add_command('db', MigrateCommand)


parse = reqparse.RequestParser()
parse.add_argument('admin', help='adminstor operator', default=False)


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}


class UserResource(Resource):
    @marshal_with(resource_fields)
    def get(self, name):
        user = LoginUser.query.filter_by(name=name).first()
        return user

    def put(self, name):
        email = request.form.get('email')
        user = LoginUser(name=name, email=email)
        db.session.add(user)
        db.session.commit()

        return {'Create': 'OK'}, 201

    def delete(self, name):
        args = parse.parse_args()
        admin = args['admin']
        if not admin:
            return 'must admin delete user'

        user = LoginUser.query.filter_by(name=name).first()
        db.session.delete(user)
        db.session.commit()

        return {'Delete': 'OK'}


api.add_resource(UserResource, '/api/<name>/')


if __name__ == '__main__':
    manager.run()

