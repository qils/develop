#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from flask import Flask, render_template, request, jsonify


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)


@app.route('/login/')
def login():
    return render_template('sigin.html')


@app.route('/signin/', methods=['POST'])
def signin():
    error = None
    username = request.form.get('username')
    password = request.form.get('password')

    if len(username) <= 6:
        error = 'username must gt 6'

    if not any(c.isupper() for c in password):
        error = 'password is error'

    if error is not None:
        return jsonify({'r': 1, 'error': error})
    else:
        return jsonify({'r': 0, 'rs': 'OK'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
