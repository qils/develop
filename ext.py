#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
manager = LoginManager()
