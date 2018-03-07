#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import os


# --------SQL Config --------#
HOSTNAME = '127.0.0.1'
DATABASE = 'r'
USERNAME = 'web'
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')
DB_URI = 'mysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
