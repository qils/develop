#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import os
import logging
import uuid


# -------- Base Config --------#
DEBUG = True
LOG_LEVEL = logging.WARN
UPLOAD_FOLDER = '/tmp/permdir'
SECRET_KEY = uuid.uuid4().hex

# -------- SQL Config --------#
HOSTNAME = '127.0.0.1'
DATABASE = 'r'
USERNAME = 'web'
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')
DB_URI = 'mysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

# -------- SQLALCHEMY Config --------#
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.0001

# ------- Flask Security Config -------- #
SECURITY_LOGIN_USER_TEMPLATE = '/root/web_develop/venv/lib/python2.7/site-packages/flask_security/templates/security/login_user.html'