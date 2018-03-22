#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import msgpack
import json
import config
import redis
from flask import Flask, request, jsonify
from ext import db
from Unit4.models import PasteFile


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)
db.init_app(app)
conn = redis.StrictRedis(host='127.0.0.1', port=6379)

max_count = 50


def default(obj):
    if isinstance(obj, PasteFile):
        return msgpack.ExtType(42, obj.to_dict())


def ext_hook(code, data):
    if code == 42:
        return PasteFile.from_dict(data)


@app.before_first_request
def before_first_request():
    db.drop_all()
    db.create_all()


@app.route('/pastedfile/', methods=['POST'])
def pastedfile():
    name = request.form.get('name')
    uploaded_file = PasteFile(name)
    db.session.add(uploaded_file)
    db.session.commit()

    print uploaded_file
    packed = msgpack.packb(msgpack.ExtType(42, uploaded_file.to_dict()))
    conn.lpush('last_files_msg', packed)
    conn.ltrim('last_files_msg', 0, max_count - 1)
    return jsonify({'ok': 0}), 201


@app.route('/get_last_files/')
def get_last_files():
    start = request.args.get('start', default=0, type=int)
    limit = request.args.get('limit', default=20, type=int)
    picked_files = conn.lrange('last_files_msg', start, start + limit - 1)

    fds = [msgpack.unpackb(each_file, ext_hook=ext_hook) for each_file in picked_files]
    return json.dumps([{'file_id': p.id, 'file_name': p.name} for p in fds])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)


