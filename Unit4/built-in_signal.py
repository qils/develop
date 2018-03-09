#!/usr/bin/env python
# --*-- coding: utf-8 --

import config
from datetime import datetime
from log_module import log_module

from flask import Flask, render_template, request
from flask import template_rendered
from flask import request_started, request_finished, got_request_exception
from flask import request_tearing_down, appcontext_tearing_down


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)
app.logger.addHandler(log_module(app.config['LOG_LEVEL']))


def log_template_render(sender, template, context, **extra):
    sender.logger.warn('template name: {}, content: {}'.format(template.name, context))


template_rendered.connect(log_template_render, app)


def log_request_start(sender, **extra):
    sender.logger.warn('request context start, remote address: {}'.format(request.remote_addr))


request_started.connect(log_request_start, app)


@app.route('/')
def index():
    return render_template('index.html', time=datetime.now(), alist=['a', 'b', 'c'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
