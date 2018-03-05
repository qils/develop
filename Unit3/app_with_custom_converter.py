#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import urllib
from flask import Flask
from werkzeug.routing import BaseConverter


app = Flask(__name__)


class ListConverter(BaseConverter):
    def __init__(self, url_map, seprator=u'+'):
        super(ListConverter, self).__init__(url_map)
        self.seprator = urllib.unquote(seprator)

    def to_python(self, value):
        return value.split(self.seprator)

    def to_url(self, values):
        return self.seprator.join(BaseConverter.to_url(self, value) for value in values)


app.url_map.converters['list'] = ListConverter


@app.route('/list/<list:args>/')
def list1(args):
    return '{} {}'.format(args[0], args[1]), 200, [{'Test': 'Flask'}]


@app.route('/list/<list(seprator=u'&'):args>/')
def list2(args):
    return '{} {}'.format(args[0], args[1])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
