#!/usr/bin/env python
# --*-- coding: utf-8 --*--

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

    conn.lpush('last_files', uploaded_file.id)
    conn.ltrim('last_files', 0, max_count - 1)

    return jsonify({'ok': 0}), 201


@app.route('/get_last_files/')
def get_last_files():
    start = request.args.get('start', default=0, type=int)
    limit = request.args.get('limit', default=20, type=int)
    fds = conn.lrange('last_files', start, start + limit - 1)

    return json.dumps([{file.id, file.name} for file in
                       PasteFile.query.filter(PasteFile.id.in_(fds)).all()])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)


