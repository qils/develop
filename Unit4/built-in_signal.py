#!/usr/bin/env python
# --*-- coding: utf-8 --

import config
from log_module import log_module

from flask import Flask, render_template
from flask import template_rendered
from flask import request_started, request_finished, got_request_exception
from flask import request_tearing_down, appcontext_tearing_down


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(config)
app.logger.addHandler(log_module(app.config['LOG_LEVEL']))


def log_template_render(sender, template, context, **extras):
    sender.logger.warn('template name: {}, content: {}'.format(template.name, context))


template_rendered.connect(log_template_render, app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
