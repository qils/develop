#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import urllib
from flask import Flask
from werkzeug.routing import BaseConverter


app = Flask(__name__)


class ListConverter(BaseConverter):
    def __init__(self, url_map, seprators=u'+'):
        super(ListConverter).__init__(self, url_map)
        self.seprators = urllib.unquote(seprators)

    def to_python(self, value):
        return value.split(self.seprators)

    def to_url(self, values):
        return self.seprators.join(BaseConverter.to_url(self, value) for value in values)

app.url_map.converters['list'] = ListConverter


@app.route('/list/<list:args>/')
def list1():
    return '{} {}'.format(args[0], args[1])


@app.route('/list/<list(seprators=u''):args>')
def list2():
    return '{} {}'.format(args[0], args[1])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
