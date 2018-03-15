#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_restful import Api


db = SQLAlchemy()
manager = LoginManager()
debugtoolbar = DebugToolbarExtension()
api = Api()

