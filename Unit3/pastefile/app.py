#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from utils import get_file_path, humanize_bytes
from flask import Flask, request, render_template, abort, jsonify
from werkzeug.wsgi import SharedDataMiddleware

from ext import db
from models import PasteFile


app = Flask(__name__, template_folder='../../templates', static_folder='../../static')
app.config.from_object(config)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/i/': get_file_path()})
db.init_app(app)


@app.before_first_request
def before_first_request():
    db.drop_all()
    db.create_all()


@app.after_request
def after_reqeust(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        upload_file = request.files.get('file')
        w = request.form.get('w')
        h = request.form.get('h')

        if not upload_file:
            abort(400)

        if w and h:
            pass
        else:
            pasted_file = PasteFile.create_by_upload_file(upload_file)

        return jsonify({
            'filename': pasted_file.filename,
            'size': humanize_bytes(pasted_file.file_size),
            'uploaded_time': str(pasted_file.uploadtime)
        })

    return render_template('pastefile.html', **locals())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
