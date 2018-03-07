#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import MySQLdb
from flask import Flask


app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
app.config.from_object('../config.py')


try:
    con = MySQLdb.conn(username=app.config['USERNAME'], password=app.config['PASSWORD'], host=app.config['HOST'], port=app.config['PORT'], db=app.config['DATABASE'])
    cur = con.cursor()
    cur.execute('select version()')
    ret = cur.fetchone()
    print ret
except MySQLdb.Error as e:
    print e.args
finally:
    if con:
        con.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
